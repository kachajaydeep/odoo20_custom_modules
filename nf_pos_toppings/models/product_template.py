# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    nf_is_topping = fields.Boolean(string="Topping?")
    topping_group_ids = fields.Many2many(
        "product.topping.groups", string="Topping Groups"
    )

    # def _load_pos_data_fields(self, config):
    #     fields = super()._load_pos_data_fields(config)
    #     fields += ["nf_is_topping", "topping_group_ids"]
    #     return fields

    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ["product_variant_id","nf_is_topping","topping_group_ids"]
        return fields
