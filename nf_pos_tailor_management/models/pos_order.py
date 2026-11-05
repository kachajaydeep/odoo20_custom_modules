# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = "pos.order"

    nf_tailor_order_ids = fields.One2many("nf.tailor.order", "pos_order_id")

    def read_pos_data(self, data, config):
        results = super().read_pos_data(data, config)
        paid_orders = self.filtered_domain(
            [("state", "in", ["paid", "done", "invoiced"])]
        )
        
        results.setdefault("nf.tailor.order", [])
        results.setdefault("nf.measurement", [])
        results.setdefault("nf.measurement.line", [])

        if not paid_orders:
            return results

        tailor_order_lines = paid_orders.mapped("nf_tailor_order_ids")
        measurement = paid_orders.mapped("lines.nf_measurement_id")
        measurement_lines = paid_orders.mapped(
            "lines.nf_measurement_id.measurement_line_ids"
        )

        results["nf.tailor.order"] = self.env["nf.tailor.order"]._load_pos_data_read(
            tailor_order_lines, config
        )
        results["nf.measurement"] = self.env["nf.measurement"]._load_pos_data_read(
            measurement, config
        )
        results["nf.measurement.line"] = self.env[
            "nf.measurement.line"
        ]._load_pos_data_read(measurement_lines, config)

        return results

    def _create_order_picking(self):
        delivery = super()._create_order_picking()        
        for record, delivery_line in zip(
            self.nf_tailor_order_ids, self.picking_ids.move_ids
        ):
            delivery_line.nf_tailor_order_id = record.id
