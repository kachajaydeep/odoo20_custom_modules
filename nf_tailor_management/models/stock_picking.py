# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import _, models, fields
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    tailor_order_id = fields.Many2one('nf.tailor.order', string="Tailor order")


    def button_validate(self):
        for rec in self:
            error_message = _("Please Manufacture the order first!")
            pos_order = (
                rec.pos_order_id
                if 'pos_order_id' in rec._fields
                else False
            )
            if not pos_order:
                if not rec.tailor_order_id:
                    raise UserError(error_message)
                elif rec.tailor_order_id.manufacturing_order_id.state not in ['done', 'cancel']:
                    raise UserError(error_message)
        res = super().button_validate()
        for rec in self:
            if rec.sale_id and rec.sale_id.tailor_order_id:
                rec.sale_id.tailor_order_id.state = "delivered"
                rec.sale_id.tailor_order_id.nf_deliver_order()
        return res