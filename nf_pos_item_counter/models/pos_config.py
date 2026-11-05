# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields #type: ignore

class ResConfigSettings(models.Model):
    _inherit = 'pos.config'
    
    nf_enable_line_count = fields.Boolean(string='Display Total Product Line')
    nf_enable_product_count = fields.Boolean(string='Display Total Product Quantity')