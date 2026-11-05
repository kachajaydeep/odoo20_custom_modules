# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo  import models, fields, api, _

class NfSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    nf_brand_id = fields.Many2one(related='product_template_id.nf_product_brand_id', string="Brand")

    
class NfSaleOrder(models.Model):
    _inherit = 'sale.order'
    
    nf_sale_order_line_brand_enable = fields.Boolean(compute="_compute_sale_order_line_brand_enable")
    nf_brand_report_enable = fields.Boolean(compute="_compute_brand_report_enable")
    
    @api.depends_context('company')
    def _compute_brand_report_enable(self):
        for rec in self:
            rec.nf_brand_report_enable = rec.env.company.nf_product_brand_report_enable
            
    @api.depends_context('company')
    def _compute_sale_order_line_brand_enable(self):
        for rec in self:
            rec.nf_sale_order_line_brand_enable = rec.env.company.nf_product_brand_on_view_enable