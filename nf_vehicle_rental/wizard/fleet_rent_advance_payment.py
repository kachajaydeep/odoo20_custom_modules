# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, _ , api
from odoo.exceptions import UserError
from datetime import  date


class FleetRentAdvancePayment(models.TransientModel):
    _name='fleet.rent.advance.payment'

    journal_id= fields.Many2one('account.journal',domain='[("type", "in", ("bank","cash"))]',required = True) 
    amount_total = fields.Float(string="Total")
    today_date = fields.Date(default=lambda self: date.today() ,string="Date Today")

    # create payment action
    def create_fleet_rent_advance_payment(self):
        active_mode = self.env.context.get('active_model')
        active_id = self.env.context.get('active_ids')
        create_fleet_rent = self.env[active_mode].browse(active_id)
        if self.amount_total == 0.0:
            raise UserError(_('Please enter the amount.'))
        payment_advance= self.env['account.payment'].create({
            'partner_id':create_fleet_rent.partner_id.id,
            'journal_id':self.journal_id.id,
            'amount':self.amount_total,
            'date':self.today_date
                })
        payment_advance.action_post()
        create_fleet_rent.account_payment_ids = [(4,payment_advance.id)]
        return {
            'name': _("Advance Payment"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.payment',
            'res_id': payment_advance.id,
            'target':'currant'
        }
    # default_get using amount_total field and amount show ('amount_residual' and 'amount_total')
    @api.model
    def default_get(self, vals):
        res = super().default_get(vals)
        active_mode = self.env.context.get('active_model')
        active_id = self.env.context.get('active_ids')
        fleet_rental_record = self.env[active_mode].browse(active_id)
        if fleet_rental_record.amount_residual:
            res['amount_total'] = fleet_rental_record.amount_residual
        else:
            res['amount_total'] = fleet_rental_record.amount_total
        return res

       
            