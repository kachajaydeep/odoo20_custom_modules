# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    nf_volume = fields.Float(string='Volume', default=0.0)
    nf_weight = fields.Float(string='Weight', default=0.0)
    nf_total_volume = fields.Float(string='Total Volume', default=0.0)
    nf_total_weight = fields.Float(string='Total Weight', default=0.0)

    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ["nf_volume", "nf_weight","nf_total_volume","nf_total_weight"]
        return fields