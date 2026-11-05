# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api, _

class PosConfig(models.Model):
    _inherit = 'pos.config'

    _nf_pos_enable_stock_restriction = fields.Boolean(string="Enable Stock restriction ? ")
    _nf_to_sale_morthan_on_hand = fields.Boolean(string="Allow to sale more than on hand ? ")