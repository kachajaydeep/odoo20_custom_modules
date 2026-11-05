# -*- coding: utf-8 -*-
# Part of NextFlowIT.

from odoo import models, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result += ['list_price']
        return result