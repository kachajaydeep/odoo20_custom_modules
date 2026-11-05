# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import fields,models,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    nf_enable_stock_request = fields.Boolean(string="Enable Stock Request From Pos",related="pos_config_id.nf_enable_stock_request",readonly=False)