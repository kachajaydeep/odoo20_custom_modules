# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    nf_pos_enable_stock_restriction = fields.Boolean(string="Enable Stock restriction")
    nf_to_sale_more_than_on_hand = fields.Boolean(string="Allow to sale more than on hand")