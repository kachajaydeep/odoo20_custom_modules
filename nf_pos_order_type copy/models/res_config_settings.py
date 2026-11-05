# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import fields,models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = "Res Config Settings"
    
    nf_pos_order_type_ids = fields.Many2many("pos.order.type", 'nf_pos_order_table_type',related='pos_config_id.nf_pos_order_type_ids',string="Pos Order Type",readonly=False)