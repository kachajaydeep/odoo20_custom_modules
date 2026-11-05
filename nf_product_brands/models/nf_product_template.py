# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api

class NfProductTemplate(models.Model):
    _inherit = 'product.template'
    
    nf_product_brand_id = fields.Many2one('product.brands', string="Brand")
    nf_product_template_brand_enable = fields.Boolean(compute="_compute_nf_product_template_brand_enable")
    
    @api.depends_context('company')
    def _compute_nf_product_template_brand_enable(self):
        for rec in self:
            rec.nf_product_template_brand_enable = rec.env.company.nf_product_brand_on_view_enable