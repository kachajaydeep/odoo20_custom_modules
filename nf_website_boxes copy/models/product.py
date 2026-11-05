# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, _, http,api
from odoo.exceptions import ValidationError

class Product(models.Model):
    _inherit = "product.template"

    nf_box_item_count = fields.Integer(string="Box Item (Qty)")

    @api.onchange("optional_product_ids")
    def _onchange_optional_product(self):
        for product in self:
            invalid_products = product.optional_product_ids.filtered(
                lambda p: (p._origin or p).nf_box_item_count
            )

            if invalid_products:
                product.optional_product_ids -= invalid_products

                return {
                    "warning": {
                        "title": _("Invalid Optional Product"),
                        "message": _(
                            "Please choose a product which does not have box items."
                        ),
                    }
                }