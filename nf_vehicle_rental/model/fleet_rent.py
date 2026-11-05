# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo.exceptions import UserError, ValidationError
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from math import ceil
import pytz
from odoo import models, fields, _, api

class FleetRent(models.Model):
    _name='fleet.rent'
    _inherit = 'mail.thread'
    _order = 'id desc'
    
    # create fields
    name = fields.Char(string="Name", default=lambda self: _('New'), readonly=True, copy=False,tracking=True)
    account_payment_ids = fields.Many2many('account.payment', copy=False, tracking=True)
    partner_id = fields.Many2one('res.partner', string="Customer" ,required=True, tracking=True)
    license_no = fields.Char(string="License",required=True, tracking=True)
    id_proof = fields.Binary(string="ID Proof",required=True)
    id_proof_name = fields.Char(string="ID Proof Name")
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company, string="Company")
    currency_id = fields.Many2one('res.currency', related="company_id.currency_id", ondelete='restrict')
    status = fields.Selection([('draft',"Draft"),
                               ('booked',"Booked"),
                               ('in_process',"In Process"),
                               ('done',"Done"),('cancel',"Cancel")
                               ], default="draft", string="Status", copy=False ,tracking=True,)
    
    rent_type = fields.Selection([('hourly',"Hourly"),
                                  ('daily',"Daily"),
                                  ('monthly',"Monthly")
                                  ], default="hourly", string="Rent Type", tracking=True)
    start_date = fields.Datetime(string="Start", default=lambda self: fields.Datetime.now(),required=True, tracking=True)
    end_date = fields.Datetime(string="End",required=True, tracking=True)
    duration = fields.Float(compute="_compute_days_count", string="Duration") 
    rent_line_ids = fields.One2many('fleet.rent.line','contract_id' , string="Rent Line")
    amount_total = fields.Float(compute="_compute_amount_total",string="Total", tracking=True, store=True)
    amount_untaxed = fields.Float(compute="_compute_amount_untaxed",string="Tax Excluded",tracking=True, store=True)
    deposit_amount =  fields.Float(compute="_compute_deposit_amount",string="Amount Deposit", tracking=True, store=True)
    invoice_id = fields.Many2one('account.move',string="Invoice", copy=False, tracking=True)
    amount_residual = fields.Float(compute="_compute_amount_residual",string="Amount Due", tracking=True, store=True)
    total_tax = fields.Float(compute="_compute_total_tax" , string="Total Tax", tracking=True, store=True)
    user_id = fields.Many2one('res.users', string="Salesperson",default=lambda self: self.env.user , required=True, tracking=True)
    
    # status view defind buttons
    def fleet_rent_draft(self):
        self.status = 'draft'
    
    def fleet_rent_booked(self):
        # status booked and sequence create
        if self.name == _('New'):
            self.name = self.env['ir.sequence'].next_by_code('fleet.rent') or _('New')
        
        # raise usererror(Vehicle is already booked)
        if not self.rent_line_ids:
            raise ValidationError(_("Vehicle details not found."))
        
        for rent_line in self.rent_line_ids:
            fleet_rent_line_ids = self.env['fleet.rent.line'].sudo().search([
                ("contract_id.status","in",('booked','in_process')),
                ('contract_id.id', '!=', self.id),
                ('vehicle_id', '=', rent_line.vehicle_id.id),
                # ('contract_id.start_date')
            ])
            for line in fleet_rent_line_ids:
                rent = line.contract_id
                if rent.start_date >= self.start_date and rent.start_date <= self.end_date \
                    or rent.end_date >= self.start_date and rent.start_date <= self.start_date :
                    raise ValidationError(_(f"{rent_line.vehicle_id.name} vehicle is already booked on {rent.name}"))
        self.status = 'booked'


    def fleet_rent_inprocess(self):
        for record in self:
            for line in record.rent_line_ids:
                line.vehicle_id.status = 'in_use'
        self.status = 'in_process'

    def fleet_rent_create_invoice(self):
        move_line_vals = []
        if self.amount_residual <= 0.0:
            for record in self:
                partner = record.partner_id.id
                for line in record.rent_line_ids:
                    vehicle_product_id = record.env.ref('nf_vehicle_rental.product_product_vehicle', raise_if_not_found=False)
                    move_line_vals.append((0,0,{
                        'name' :line.vehicle_id.name,
                        'product_id' : line.vehicle_id.vehicle_product_id.id or vehicle_product_id.id,
                        'quantity': line.duration_value,
                        'price_unit' : line.rate,
                        'tax_ids' : line.taxes_id.ids
                    }))
                move_id = self.env['account.move'].create([{
                    'partner_id': partner,
                    'invoice_date' : fields.Datetime.today(),
                    'move_type' :'out_invoice',
                    'invoice_line_ids' :move_line_vals
                }])
                record.invoice_id = move_id
                move_id.action_post()

            move_lines = self.account_payment_ids.move_id.line_ids.filtered(lambda line: line.account_type in ('asset_receivable', 'liability_payable') and not line.reconciled)
            for line in move_lines:
                move_id.js_assign_outstanding_line(line.id)
            
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'account.move',
                'res_id': move_id.id,
                'views': [(self.env.ref('account.view_move_form').id, 'form')],
                'target':'currant'
            }
        
        else:
            raise ValidationError(_('Payment is still pending'))

    def fleet_rent_done(self):
        for record in self:
            for line in record.rent_line_ids:
                line.vehicle_id.status = 'available_to_rent'
        self.status = 'done'
    
    def fleet_rent_cancel(self):
        for record in self:
            for payment_line in record.account_payment_ids:
                if payment_line.state in ('in_process','paid'):
                    raise UserError(_("You can't cancel the rent due to payment is created."))
            if record.status == 'in_process':
                for line in record.rent_line_ids:
                    line.vehicle_id.status = 'available_to_rent'
        self.status = 'cancel'

    # compute method duration 
    @api.depends('rent_type', 'start_date', 'end_date')
    def _compute_days_count(self):
        self.duration = 1
        for fleet_rent_type in self:
            if fleet_rent_type.rent_type == 'hourly':
                if(fleet_rent_type.end_date and fleet_rent_type.start_date):
                        fleet_rent_hourly = fleet_rent_type.end_date - fleet_rent_type.start_date
                        rent_hours = (fleet_rent_hourly).total_seconds() / 3600
                        fleet_rent_type.duration = rent_hours

            elif fleet_rent_type.rent_type == 'daily':
                if (fleet_rent_type.start_date and fleet_rent_type.end_date):
                    fleet_rent_daily=(fleet_rent_type.end_date - fleet_rent_type.start_date)
                    rent_days=fleet_rent_daily.days
                    fleet_rent_type.duration=rent_days
                
            elif fleet_rent_type.rent_type == 'monthly':
                if (fleet_rent_type.start_date and fleet_rent_type.end_date):
                    fleet_rent_month = relativedelta(fleet_rent_type.end_date, fleet_rent_type.start_date)
                    total_months = fleet_rent_month.years * 12 + fleet_rent_month.months
                    fleet_rent_type.duration = ceil(total_months)
                    if fleet_rent_month.days > 0:
                        total_months += 1
                        total_days =(fleet_rent_type.end_date - fleet_rent_type.start_date).days
                        fleet_rent_type.duration = total_days
            else:
                fleet_rent_type.duration = 1

    # onchange end date
    @api.onchange('start_date','rent_type')
    def _onchange_fleet_rent_end_date(self):
        self.end_date=0
        for fleet_rent_types in self:
            if fleet_rent_types.rent_type == 'hourly':
                if fleet_rent_types.start_date:
                    fleet_rent_hours = fleet_rent_types.start_date + timedelta(hours=1)
                    fleet_rent_types.end_date = fleet_rent_hours
                else:
                    fleet_rent_types.end_date = False

            elif fleet_rent_types.rent_type == 'daily':
                if fleet_rent_types.start_date:
                    fleet_rent_days = fleet_rent_types.start_date + timedelta(days=1)
                    fleet_rent_types.end_date = fleet_rent_days
                else:
                    fleet_rent_types.end_date = False
            
            elif fleet_rent_types.rent_type == 'monthly':
                if fleet_rent_types.start_date:
                    fleet_rent_month = fleet_rent_types.start_date + relativedelta(months=1)
                    fleet_rent_types.end_date = fleet_rent_month
                else:
                    fleet_rent_types.end_date = False

    # onchange rent_type
    @api.onchange('rent_type')
    def _onchange_duration_value(self):
        for fleet_rent_id in self:
            for fleet_rent_line_id in self.rent_line_ids:
                if fleet_rent_id.rent_type == 'hourly':
                    fleet_vehicle_hourly_rate = fleet_rent_line_id.vehicle_id.default_rate_hourly
                    fleet_rent_line_id.rate = fleet_vehicle_hourly_rate

                elif fleet_rent_id.rent_type == 'daily':
                    fleet_vehicle_daily_rate = fleet_rent_line_id.vehicle_id.default_rate_daily
                    fleet_rent_line_id.rate = fleet_vehicle_daily_rate
                
                elif fleet_rent_id.rent_type == 'monthly':
                    fleet_vehicle_month_rate = fleet_rent_line_id.vehicle_id.default_rate_mothly
                    fleet_rent_line_id.rate = fleet_vehicle_month_rate

                else:
                    fleet_rent_line_id.rate = 0

    @api.onchange('license_no','id_proof')
    def _onchange_license_no_and_id_proof(self):
        for record in self:
            if record.partner_id:
                record.partner_id.license_no = record.license_no
                record.partner_id.id_proof_attachment = record.id_proof
                record.partner_id.id_proof_name = record.id_proof_name
                
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for record in self:
            if record.partner_id:
                record.license_no = record.partner_id.license_no 
                record.id_proof = record.partner_id.id_proof_attachment
                record.id_proof_name = record.partner_id.id_proof_name

    def _cron_fleet_rent_record_cancel(self):
        current_date = fields.Date.today()
        fleet_rent_ids = self.env['fleet.rent'].sudo().search([("status","in",('draft','booked')),
                                                               ("end_date","<",current_date)])
        for record in fleet_rent_ids:
            if record.status == 'draft':
                record.fleet_rent_cancel()
            elif record.status == 'booked':
                if not record.account_payment_ids:
                    record.fleet_rent_cancel()

    @api.constrains('end_date','start_date')
    def _constrains_start_date_end_date(self):
        current_date = fields.Datetime.today()
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError(_('Invalid date range: end date is earlier than the start date.'))
            elif record.end_date < current_date:
                raise ValidationError(_('The start date and end date must not be earlier than today.'))

    # amount untaxed
    @api.depends('rent_type','rent_line_ids.subtotal')
    def _compute_amount_untaxed(self):
        self.amount_untaxed = 0.0
        for record in self:
            for line in record.rent_line_ids:
                record.amount_untaxed = line.subtotal + record.amount_untaxed
    
    # deposit amount payment
    @api.depends('amount_residual','account_payment_ids')
    def _compute_deposit_amount(self):
        self.deposit_amount = 0.0
        for record in self:
            total_deposit = 0.0
            for payment_amount in record.account_payment_ids:
                total_deposit += payment_amount.amount 
            record.deposit_amount = total_deposit

    # amount residual (amount due)
    @api.depends('amount_total','deposit_amount')
    def _compute_amount_residual(self):
        self.amount_residual = 0.0
        for record in self:
            total_amount_residual = record.amount_total - record.deposit_amount
            record.amount_residual = total_amount_residual
           
    # total taxes
    @api.depends('rent_type','rent_line_ids')
    def _compute_total_tax(self):
        self.total_tax = 0.0
        for record in self:
            line_total_tax = 0.0
            for line in record.rent_line_ids:
                line_total_tax += line.tax_total
            record.total_tax = line_total_tax

    # amount total
    @api.depends('rent_type','amount_untaxed','total_tax')
    def _compute_amount_total(self):
        self.amount_total = 0
        for record in self:
            if record.total_tax:
                total = record.amount_untaxed + record.total_tax
                record.amount_total =  total  + record.amount_total 
            else:
                record.amount_total = record.amount_untaxed


    # button_box 
    def action_payments_view(self):
        return self.account_payment_ids._get_records_action(name=_("Payments"))

    def action_invoice_view(self):
        return self.invoice_id._get_records_action(name=_("Invoice"))