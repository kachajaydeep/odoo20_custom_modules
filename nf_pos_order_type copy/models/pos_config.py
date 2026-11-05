# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import fields,models

class PosConfig(models.Model):
    _inherit = 'pos.config'
    _description = "Pos Config"
    
    nf_pos_order_type_ids = fields.Many2many("pos.order.type", 'nf_pos_order_table_type',string="Pos Order Type",readonly=False)
    