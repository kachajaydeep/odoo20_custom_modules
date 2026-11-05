# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api, _

class NfPurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    
    amount_to_bill = fields.Monetary(string="Un-invoiced Balance", compute='_compute_amount_to_bill', currency_field='currency_id', store=True)
    amount_bill = fields.Monetary(string="Already invoiced", compute='_compute_amount_bill', currency_field='currency_id', store=True)
    
    @api.depends('order_line.amount_to_bill')
    def _compute_amount_to_bill(self):
        self.amount_to_bill = 0.0
        for order in self:
            order.amount_to_bill = sum(order.order_line.mapped('amount_to_bill'))

            
    @api.depends('order_line.amount_bill')
    def _compute_amount_bill(self):
        self.amount_bill = 0.0
        for order in self:
            order.amount_bill = sum(order.order_line.mapped('amount_bill'))
            
    
    def action_create_invoice(self, grouped=False):
        return {
            'name'      : _('Create Bill(s)'),
            'type'      : 'ir.actions.act_window',
            'res_model' : 'purchase.advance.payment.bill',
            'view_mode' : 'form',
            'views'     : [(False, 'form')],   # Required
            'target'    : 'new',
            'binding_model_id': False,         # Prevents binding issues
            'context'   : {
                'default_purchase_order_ids': self.ids,
                'active_ids'                : self.ids,
                'active_model'              : 'purchase.order',
            }
        }
            

    def copy_data(self, default=None):
        data = super().copy_data(default=default)
        for vals in data:
            if 'order_line' in vals:
                filtered = []
                for line in vals['order_line']:
                    line_vals = {}

                    if isinstance(line, (list, tuple)) and len(line) >= 3:
                        line_vals = line[2] or {}
                    elif hasattr(line, '_values'):
                        line_vals = line._values or {}
                    elif isinstance(line, dict):
                        line_vals = line

                    if not line_vals.get('is_downpayment', False):
                        filtered.append(line)

                vals['order_line'] = filtered
        return data
