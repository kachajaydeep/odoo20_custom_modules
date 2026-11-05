# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_pos_salesperson = fields.Boolean(string="SalesPerson")
    commission_rule_ids = fields.Many2many("pos.commission.rules", string="Commission")

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields += ["is_pos_salesperson", "commission_rule_ids"]
        return fields


class HrEmployeepublic(models.Model):
    _inherit = "hr.employee.public"

    is_pos_salesperson = fields.Boolean(
        string="SalesPerson", related="employee_id.is_pos_salesperson"
    )
    commission_rule_ids = fields.Many2many(
        "pos.commission.rules",
        string="Commission",
        related="employee_id.commission_rule_ids",
    )
