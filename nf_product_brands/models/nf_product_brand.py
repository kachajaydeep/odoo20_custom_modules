# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api, _

class NfProductBrands(models.Model):
    _name = 'product.brands'
    _rec_name = 'nf_name'
    
    nf_name = fields.Char(string="Name", required=True, copy=False)
    nf_sequence = fields.Integer(string="Sequence", required=True)
    active = fields.Boolean(string="Active", default=True)
    nf_image = fields.Binary(string="Image", attachment=True)
    nf_product_ids = fields.One2many("product.template", "nf_product_brand_id", string="Brand Product")
    nf_description = fields.Html(string="Description")