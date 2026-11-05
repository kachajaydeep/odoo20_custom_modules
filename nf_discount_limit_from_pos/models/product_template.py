# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    nf_discount_type = fields.Selection(
        [("percentage", "Percentage"), ("fixed", "Fixed")],
        default="fixed",
        string="Discount Type",
    )
    nf_discount_limit = fields.Float(string="Discount Limit")

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields += ["nf_discount_type", "nf_discount_limit"]
        return fields
