# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class ProductToppingGroups(models.Model):
    _name = "product.topping.groups"
    _order = "sequence asc"

    name = fields.Char(string="Name", required=True)
    product_topping_ids = fields.Many2many(
        "product.product",
        "topping_group_product_product_rel",
        string="Toppings",
        domain="[('nf_is_topping', '=', True)]",
        required=True,
    )

    sequence = fields.Integer()

    @api.model
    def _load_pos_data_domain(self, data, config):
        return []

    @api.model
    def _load_pos_data_fields(self, config):
        return []

    def _load_pos_data_search_read(self, record, config):
        domain = self._load_pos_data_domain(record, config)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain, fields)
        return records


# class ProductProduct(models.Model):
#     _inherit = "product.product"

#     nf_is_topping = fields.Boolean(string="Topping?")
#     topping_group_ids = fields.Many2many(
#         "product.topping.groups", string="Topping Groups"
#     )

#     def _load_pos_data_fields(self, config):
#         fields = super()._load_pos_data_fields(config)
#         fields += ["nf_is_topping", "topping_group_ids"]
#         return fields
