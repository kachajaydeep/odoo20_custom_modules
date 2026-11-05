# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models,fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    nf_product_search_by_vendor = fields.Boolean(string="Enable Product Search Using Vendor",related="pos_config_id.nf_product_search_by_vendor",readonly=False)