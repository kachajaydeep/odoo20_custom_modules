# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields #type: ignore

class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    nf_barcode_id = fields.Char(string='Barcode')
    is_exchange = fields.Boolean(string='Is Exchange')
    nf_enable_receipt_barcode = fields.Boolean(related="config_id.nf_enable_receipt_barcode",store=False)
    nf_return_exchange_reason = fields.Char(string="Return/Exchange Reason")
    
    def action_pos_order_paid(self):
        result = super().action_pos_order_paid()
        for order in self:
            if order.pos_reference and not order.nf_barcode_id:
                if order.nf_enable_receipt_barcode and not order.is_refund and not order.is_exchange:
                    prefix = order.config_id.nf_barcode_prefix
                    order.nf_barcode_id = prefix + '-' + order.pos_reference
        return result