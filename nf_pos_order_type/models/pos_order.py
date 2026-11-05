# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import fields,models,api

class PosOrder(models.Model):
    _inherit = "pos.order"
    
    nf_pos_order_type_id = fields.Many2one("pos.order.type",string="Pos Order Type")
    nf_name = fields.Char(string="Pos Order Type Name")
    