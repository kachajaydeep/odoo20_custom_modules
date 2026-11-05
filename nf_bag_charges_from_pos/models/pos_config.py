# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields,api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    nf_enable_bag_charges = fields.Boolean(string="Enable Bag Charges")
    nf_carry_bag_category_id = fields.Many2one('pos.category',string="Carry Bag Category",domain=[])

    # @api.model
    # def _load_pos_data_fields(self, config_id):
    #     result = super()._load_pos_data_fields(config_id)
    #     result += ['nf_enable_bag_charges', 'nf_carry_bag_category_id']
    #     return result