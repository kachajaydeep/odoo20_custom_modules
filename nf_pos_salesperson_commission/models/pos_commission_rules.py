# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api, _


class PosCommisionRules(models.Model):
    _name = "pos.commission.rules"

    name = fields.Char(
        string="Commission Rule",
        required=True,
        default=lambda self: _("New"),
        readonly=True,
        copy=False,
    )
    employee_ids = fields.Many2many("hr.employee", string="Salespersons")
    product_ids = fields.Many2many("product.product", string="Product")
    commission_type = fields.Selection(
        [("percentage", "Percentage"), ("fixed", "Fixed")],
        default="fixed",
        string="Commission Type",
    )
    amount = fields.Float(string="Commission")
    active = fields.Boolean(string="Active", default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for create_new_commission_rule in vals_list:
            if create_new_commission_rule.get("name", _("New")) == _("New"):
                create_new_commission_rule["name"] = self.env[
                    "ir.sequence"
                ].next_by_code("pos.commission.rules")
        return super(PosCommisionRules, self).create(vals_list)

    @api.model
    def _load_pos_data_domain(self, data, config):
        return []

    def _load_pos_data_fields(self, config):
        return []

    def _load_pos_data_search_read(self, records, config):
        domain = self._load_pos_data_domain(records, config)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain, fields)
        return records
