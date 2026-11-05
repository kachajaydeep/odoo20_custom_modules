# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api

class NfSaleReport(models.Model):
    
    _inherit = "sale.report"
    
    nf_product_brand_id = fields.Many2one(
        "product.brands",
        string="Brand",
        readonly=True
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['nf_product_brand_id'] = "t.nf_product_brand_id" 
        return res
    
    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += ", t.nf_product_brand_id"
        return res