# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models,fields

class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    nf_product_search_by_vendor = fields.Boolean(string="Enable Product Search Using Vendor")