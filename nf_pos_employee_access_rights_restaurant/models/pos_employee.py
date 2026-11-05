# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    nf_hide_cancel_order_button = fields.Boolean(string="Hide Cancel Order Button")
    nf_hide_split_button = fields.Boolean(string="Hide Split Button")
    nf_hide_merge_button = fields.Boolean(string="Hide Transfer/Merge Button")
    nf_hide_create_product = fields.Boolean(string="Hide Create Product")
    nf_hide_edit_plan = fields.Boolean(string="Hide Edit Plan")
    nf_hide_switch_floor_view = fields.Boolean(string="Hide Switch Floor View")
    nf_hide_bill = fields.Boolean(string="Hide Bill Button")
    nf_hide_guest_btn = fields.Boolean(string="Hide Guests Button")

    @api.model
    def _load_pos_data_fields(self, config):
        result = super()._load_pos_data_fields(config)
        result += [
            "nf_hide_cancel_order_button",
            "nf_hide_split_button",
            "nf_hide_merge_button",
            "nf_hide_create_product",
            "nf_hide_bill",
            "nf_hide_guest_btn",
            "nf_hide_edit_plan",
            "nf_hide_switch_floor_view",
        ]
        return result
