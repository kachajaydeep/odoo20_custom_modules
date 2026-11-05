# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"
    _description = "Pos Order Line"

    nf_mrp_bom_id = fields.Many2one("nf.mrp.bom")
    nf_bom_component_ids = fields.One2many(
        "nf.bom.component", "nf_pos_order_line_id", string="Bom Components"
    )
    nf_measurement_id = fields.Many2one("nf.measurement")
    nf_delivery_date = fields.Date(string="Delivery Date")

    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += [
            "nf_bom_component_ids",
            "product_id",
            "nf_mrp_bom_id",
            "nf_measurement_id",
            "nf_delivery_date",
        ]
        return fields
