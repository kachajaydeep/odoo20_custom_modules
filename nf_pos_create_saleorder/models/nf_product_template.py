# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api


class NfProductTemplate(models.Model):
    _inherit = "product.template"

    nf_demo_product_for_sale_section = fields.Boolean()

    @api.model
    def _load_pos_data_fields(self, config):
        res = super()._load_pos_data_fields(config)
        res += ["nf_demo_product_for_sale_section"]
        return res

    @api.model
    def _load_pos_data_read(self, records, config):
        res = super()._load_pos_data_read(records, config)
        res += self.env.ref("nf_pos_create_saleorder.nf_demo_product_for_section").read(
            self._load_pos_data_fields(config)
        )
        return res
