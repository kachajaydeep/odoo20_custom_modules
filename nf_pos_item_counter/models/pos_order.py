# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields #type: ignore

class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    nf_line_count = fields.Integer(string='Total Order Line')
    nf_product_count = fields.Integer(string='Total Product Quantity')