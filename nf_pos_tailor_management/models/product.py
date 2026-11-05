# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = "product.product"
    _description = "Product Product"

    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ["id", "bom_count", "bom_ids"]
        return fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ["display_name", "name"]
        return fields
