# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 


from odoo import models, fields, api

class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    nf_pos_enable_stock_info = fields.Boolean(string="Enable Stock Information")