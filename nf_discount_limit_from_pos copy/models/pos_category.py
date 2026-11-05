# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class PosCategory(models.Model):
    _inherit = "pos.category"

    nf_discount_type = fields.Selection(
        [("percentage", "Percentage"), ("fixed", "Fixed")],
        default="fixed",
        string="Discount Type",
    )
    nf_discount_limit = fields.Float(string="Discount Limit")

    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ["nf_discount_type", "nf_discount_limit"]
        return fields
