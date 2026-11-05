# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    nf_employee_id = fields.Many2one("hr.employee", string="SalesPerson")
    pos_commission_line_ids = fields.One2many("pos.commission.line", "order_line_id")
    commission_amount = fields.Float()

    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ["nf_employee_id", "pos_commission_line_ids", "commission_amount"]
        return fields


class PosOrder(models.Model):
    _inherit = "pos.order"
