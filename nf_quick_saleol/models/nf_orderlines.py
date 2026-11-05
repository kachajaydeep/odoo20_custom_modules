# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from email.policy import default
from odoo import models, fields, api

class SaleOrderinherit(models.Model):
    _inherit = 'sale.order'

    nf_product_id = fields.Many2one('product.product', string='Product ')
    nf_enable_quick_sol = fields.Boolean(related='company_id.nf_enable_quick_sol')
    nf_qty = fields.Integer(string='Quantity')
    nf_product_price = fields.Integer(string='Price')

    @api.onchange('nf_product_id')
    def onchangeProductLine(self):
        if self.nf_product_id:
            self.write({'order_line': [(0, 0, { 'order_id': self.id, 'product_id': self.nf_product_id.id, 'name': self.nf_product_id.display_name, 'product_uom_id': self.nf_product_id.uom_id, 'product_uom_qty': 1, 'tax_ids': self.nf_product_id.taxes_id, 'price_unit': self.nf_product_id.list_price })]})
            self.nf_product_id = False

class ComapanyInherit(models.Model):
    _inherit = 'res.company'

    nf_enable_quick_sol = fields.Boolean()

class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    _nf_enable_quick_sale_orderline = fields.Boolean(string='Enable Quick Sale Orderline',readonly=False, related='company_id.nf_enable_quick_sol')