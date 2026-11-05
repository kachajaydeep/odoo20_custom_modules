# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:
            if picking.move_ids:
                tailor_orders = picking.move_ids.mapped("nf_tailor_order_id")

                for order in tailor_orders:
                    if not order:
                        continue

                    if not order.manufacturing_order_id:
                        raise UserError("Please manufacture the order first...")

                    if order.manufacturing_order_id.state != "done":
                        raise UserError("Please complete the manufacturing order first")

        res = super().button_validate()

        for picking in self:
            if picking.move_ids:
                tailor_orders = picking.move_ids.mapped("nf_tailor_order_id")

                for order in tailor_orders:
                    if order:
                        order.state = "delivered"
                        order.nf_deliver_order()

        return res
