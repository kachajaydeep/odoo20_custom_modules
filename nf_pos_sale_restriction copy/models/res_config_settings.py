# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api, _

class ReesPosConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    
    nf_pos_enable_stock_restriction = fields.Boolean(related="pos_config_id.nf_pos_enable_stock_restriction", readonly=False)
    nf_to_sale_more_than_on_hand = fields.Boolean(related="pos_config_id.nf_to_sale_more_than_on_hand", readonly=False)