# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields 

class NfMultiBarcode(models.Model):
    _name = 'nf.multi.barcode'

    name = fields.Char(string="Barcode", required=True)
    nf_product_id = fields.Many2one('product.product', string="Product")
    nf_product_template_id = fields.Many2one('product.template', string="Product")