# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields, api

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
    pricelist_name = fields.Char(related='pricelist_id.name', string='Pricelist Name')
    nf_line_total = fields.Char()
    
    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config) # type: ignore
        fields += ['pricelist_id','pricelist_name','nf_line_total']
        return fields