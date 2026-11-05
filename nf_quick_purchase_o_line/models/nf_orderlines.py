# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.
 
from odoo import models, fields, api

class PurchaseOrderinherit(models.Model):
    _inherit = 'purchase.order'

    nf_product_id = fields.Many2one('product.product', string='Product ')
    nf_enable_quick_pol = fields.Boolean(related='company_id.nf_enable_quick_pol')
    nf_qty = fields.Integer(string='Quantity')
    nf_product_price = fields.Integer(string='Price')

    @api.onchange('nf_product_id')
    def onchangeProductLine(self):
        if self.nf_product_id:
            if self.nf_product_id.id in self.order_line.product_id.ids:
                for line in self.order_line:
                    if line.product_id.id == self.nf_product_id.id:
                        line.write({ 'product_qty': line.product_qty + 1, })
            else:
                self.write({'order_line': [(0, 0, { 'order_id': self.id, 'product_id': self.nf_product_id.id, 'name': self.nf_product_id.display_name, 'uom_id': self.nf_product_id.uom_id, 'product_qty': 1,'date_planned': fields.Date.today(),'price_unit': self.nf_product_id.list_price })]})
            self.nf_product_id = False

class ComapanyInherit(models.Model):
    _inherit = 'res.company'

    nf_enable_quick_pol = fields.Boolean()

class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    _nf_enable_quick_purchase_orderline = fields.Boolean(string='Enable Quick Purchase Orderline',readonly=False, related='company_id.nf_enable_quick_pol')