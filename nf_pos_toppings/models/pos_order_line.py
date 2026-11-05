# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    nf_child_orderline_id = fields.Many2one("pos.order.line")

    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ["nf_child_orderline_id"]
        return fields
