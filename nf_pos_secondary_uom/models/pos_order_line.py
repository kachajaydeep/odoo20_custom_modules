# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api    #type: ignore

class PosOrderLineInherited(models.Model):
    _inherit = 'pos.order.line'
    
    selected_uom_id = fields.Many2one('uom.uom', string='Selected UOM ID', help="Secondary UOM selected at POS for this line")

    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ['selected_uom_id']
        return fields