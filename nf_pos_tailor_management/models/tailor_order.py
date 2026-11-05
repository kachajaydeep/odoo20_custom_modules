# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api, _, Command

class TailorOrder(models.Model):
    _name = "nf.tailor.order"
    _inherit = ["pos.load.mixin","nf.tailor.order"]
    _description = "Tailor Order"

    pos_order_id = fields.Many2one("pos.order", string="Pos Order")
    pos_order_line_id = fields.Many2one("pos.order.line", string="Pos Order Line")
    pos_order_count = fields.Integer(compute="_compute_pos_order", string="Pos Order")
    stock_picking_count = fields.Integer(
        compute="_compute_stock_picking", string="Delivery"
    )
    account_move_count = fields.Integer(compute="_compute_invoice", string="Invoice")

    @api.model
    def _load_pos_data_domain(self, data):
        return []

    @api.model
    def _load_pos_data_fields(self, config):
        return [
            "id",
            "name",
            "customer_id",
            "order_date",
            "delivery_date",
            "product_id",
            "pos_order_id",
            "tailor_line_ids",
            "bom_id",
            "measurement_id",
            "manufacturing_order_id",
            "sale_order_id",
            "sale_order_count",
            "manufacturing_order_count",
            "picking_count",
            "currency_id",
            "measurement_line_ids",
            "state",
            "write_date",
        ]

    def _load_pos_data_search_read(self, data, config):
        domain = self._load_pos_data_domain(data)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain, fields)
        return records

    @api.model
    def _load_pos_data_read(self, records, config):
        fields = self._load_pos_data_fields(config)
        return records.read(fields, load=False)

    def action_view_pos_orders(self):
        recent_pos_orders = self.env["ir.actions.actions"]._for_xml_id(
            "nf_pos_tailor_management.nf_action_pos_form"
        )
        recent_pos_order_id = self.env["pos.order"].search(
            [("id", "=", self.pos_order_id.id)], limit=1
        )

        recent_pos_orders.update(
            {
                "view_mode": "form",
                "res_id": recent_pos_order_id.id,
                "views": [(False, "form")],
            }
        )
        return recent_pos_orders

    @api.model
    def nf_create_tailor_order_from_pos(self, vals):
        tailor_order = self.create(vals)
        return tailor_order.id

    def _compute_pos_order(self):
        self.pos_order_count = 0
        pos_order_count = self.env["pos.order"].search_count(
            [("nf_tailor_order_ids.pos_order_id", "=", self.pos_order_id.id)]
        )
        self.pos_order_count = pos_order_count

    def action_view_delivery_order(self):
        action = {
            "name": _("Delivery Order(s)"),
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "target": "current",
            "context": {"active_tailor_order_id": self.id},
        }
        picking_ids = self.pos_order_id.picking_ids.ids
        if len(picking_ids) == 1:
            action["res_id"] = picking_ids[0]
            action["view_mode"] = "form"
        else:
            action["view_mode"] = "list,form"
            action["domain"] = [("id", "in", picking_ids)]
        return action

    def _compute_stock_picking(self):
        self.stock_picking_count = 0

        if self.pos_order_id and self.pos_order_id.picking_ids:
            self.stock_picking_count = len(self.pos_order_id.picking_ids)

    def action_view_invoice(self):
        recent_invoice_order = self.env["ir.actions.actions"]._for_xml_id(
            "nf_pos_tailor_management.nf_action_account_move_form"
        )
        recent_invoice_order.update(
            {
                "view_mode": "form",
                "res_id": self.pos_order_id.account_move.id,
                "views": [(False, "form")],
            }
        )
        return recent_invoice_order

    def _compute_invoice(self):
        self.account_move_count = 0

        if self.pos_order_id.account_move.id:
            self.account_move_count = 1 if self.pos_order_id.account_move else 0

    @api.depends("measurement_id")
    def _compute_measurement_lines(self):
        for record in self:
            line_vals_list = []
            for line_vals in record.measurement_id.measurement_line_ids.read(
                load=False
            ):
                line_vals.pop("id", None)
                line_vals.pop("measurement_id", None)
                line_vals.pop("tailor_order_id", None)
                line_vals_list.append(Command.create(line_vals))
            record.measurement_line_ids = [Command.clear()] + line_vals_list

    @api.depends("measurement_id")
    def _compute_measurement_design_lines(self):
        for record in self:
            design_vals_list = []
            for line_vals in record.measurement_id.measurement_design_ids.read(
                load=False
            ):
                line_vals.pop("id", None)
                line_vals.pop("measurement_id", None)
                line_vals.pop("tailor_order_id", None)
                design_vals_list.append(Command.create(line_vals))
            record.design_ids = [Command.clear()] + design_vals_list