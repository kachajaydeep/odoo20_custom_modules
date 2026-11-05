# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo  import models, fields, api, _
from odoo.exceptions import UserError

class NfSaleOrder(models.Model):
    _inherit = 'sale.order'
    
    nf_enable_one_click_sale = fields.Boolean(related='company_id.nf_enable_one_click_sale', store=False )
    nf_pay_invoice = fields.Boolean(related='company_id.nf_pay_invoice', store=False )
    nf_journal_id = fields.Many2one('account.journal', string='Payment Journal', domain="[('type', 'in', ['cash', 'bank']), ('company_id', '=', company_id)]",  copy=False, compute='_compute_nf_journal_id', store=True, readonly=False,)
    nf_payment_amount = fields.Monetary(compute='_compute_nf_payment_amount', string='Payment Amount', store=True, readonly=False, currency_field='currency_id', copy=False)
    nf_remaining_amount = fields.Monetary(compute="_compute_nf_remaining_amount", string='Remaining Amount', store=True, currency_field='currency_id', copy=False)
    
    @api.depends('company_id')
    def _compute_nf_journal_id(self):
        for record in self:
            if not record.nf_journal_id:
                record.nf_journal_id = self.env['account.journal'].search([
                    ('type', '=', 'bank'),
                    ('company_id', '=', record.company_id.id)
                ], limit=1)
        
    # payment amount
    @api.depends('amount_total')
    def _compute_nf_payment_amount(self):
        self.nf_payment_amount = 0.0
        for record in self:
            record.nf_payment_amount = record.amount_total
    
    # remaining amount
    @api.depends('amount_total','nf_payment_amount', 'invoice_ids', 'invoice_ids.amount_residual', 'invoice_ids.payment_state')
    def _compute_nf_remaining_amount(self):
        for record in self:
            invoices = record.invoice_ids.filtered(
                lambda inv: inv.state != 'cancel'
            )
            if invoices:
                # Show amount_residual from invoice
                record.nf_remaining_amount = sum(invoices.mapped('amount_residual'))
            else:
                # No invoice yet -> show amount_total - nf_payment_amount
                record.nf_remaining_amount = record.amount_total - record.nf_payment_amount

            
    def action_one_click_sale(self):
        stock_warnings = []
         
        for record in self:
            if record.state == 'draft':
                record.action_confirm()
            elif record.state == 'sent':
                record.action_confirm()
                
            #  delivery validate
            if record.company_id.nf_validate_delivery == True:
                pickings = self.env['stock.picking'].sudo().search([
                    ('sale_id', '=', record.id),
                    ('picking_type_code', '=', 'outgoing'),
                    ('state', '!=', 'cancel')
                ])
                for picking in pickings:                    
                    # # Already validated, skip
                    if picking.state == 'done':
                        continue

                    # Reserve stock
                    if picking.state != 'assigned':
                        picking.action_assign()

                    # Set available quantity
                    for move in picking.move_ids.filtered(lambda m: m.state not in ('done', 'cancel')):
                        move.quantity = sum(move.move_line_ids.mapped('quantity'))                                
                    
                    # Validate
                    if any(m.quantity > 0 for m in picking.move_ids):
                        try:
                            res = picking.with_context(
                                skip_backorder=True,
                                send_sms=False,
                            ).button_validate()

                            if isinstance(res, dict):
                                res_model = res.get("res_model")
                                ctx = res.get("context", {})

                                # SMS Wizard
                                if res_model == "confirm.stock.sms":
                                    sms_wizard = self.env["confirm.stock.sms"].with_context(**ctx).create({})

                                    if hasattr(sms_wizard, "action_just_validate"):
                                        sms_wizard.action_just_validate()
                                    elif hasattr(sms_wizard, "action_confirm"):
                                        sms_wizard.action_confirm()
                                    elif hasattr(sms_wizard, "action_done"):
                                        sms_wizard.action_done()
                                    elif hasattr(sms_wizard, "action_validate"):
                                        sms_wizard.action_validate()
                                    else:
                                        picking.sudo()._action_done()

                                # Backorder Wizard
                                elif res_model == "stock.backorder.confirmation":
                                    self.env["stock.backorder.confirmation"].with_context(**ctx).create({
                                        "pick_ids": [(4, picking.id)]
                                    }).process_cancel_backorder()

                        except UserError:
                            # Let Odoo display its own official validation message
                            raise                              
                        
            # invoice create                     
            if record.company_id.nf_create_invoice == True:
                if record.invoice_status == 'to invoice':
                    invoices = record.sudo()._create_invoices()
                    if invoices:
                        invoices.sudo().action_post()  # Confirm invoice -> posted
                else:
                    invoices = record.sudo()._create_invoices()
                    if invoices:
                        invoices.sudo().action_post()  # Confirm invoice -> posted
                        
            # invocie payment            
            if record.company_id.nf_pay_invoice == True:
                invoices = record.invoice_ids.filtered(
                    lambda inv: inv.state == 'posted' and inv.payment_state != 'paid'
                )
                for invoice in invoices:
                    # Use record journal or fallback to default
                    journal = record.nf_journal_id or self.env['account.journal'].sudo().search([
                        ('type', 'in', ['cash', 'bank']),
                        ('company_id', '=', record.company_id.id)
                    ], limit=1)

                    wizard = self.env['account.payment.register'].with_context(
                        active_model='account.move',
                        active_ids=invoice.ids
                    ).sudo().create({
                        'journal_id': journal.id,
                        'amount': record.nf_payment_amount or invoice.amount_residual,
                        'payment_date': fields.Date.today(),
                    })
                    wizard.sudo().action_create_payments()