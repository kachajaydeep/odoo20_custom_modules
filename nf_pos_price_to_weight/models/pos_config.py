# -*- coding: utf-8 -*-
# Part of NextFlowIT.

from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    def _default_nft_price_to_weight_selection(self):
        return self.env.ref("product.field_product_product__list_price")
    
    nft_price_to_weight_selection = fields.Many2one("ir.model.fields", string="Select Price To Weight", domain='[("model", "=", "product.product"), ("ttype", "=", "float")]',
        required=True, ondelete='cascade', index=True, default=lambda x: x._default_nft_price_to_weight_selection() )

    nft_price_to_weight_selected = fields.Char(related="nft_price_to_weight_selection.name")