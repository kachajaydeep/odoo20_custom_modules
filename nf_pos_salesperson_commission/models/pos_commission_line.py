# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api, _


class PosCommissionLine(models.Model):
    _name = "pos.commission.line"

    name = fields.Char(
        string="Commission Line",
        default=lambda self: _("New"),
        readonly=True,
        copy=False,
    )
    commission_rule_id = fields.Many2one(
        "pos.commission.rules", string="Commission Rule"
    )
    order_line_id = fields.Many2one("pos.order.line", string="Order Line")
    employee_id = fields.Many2one("hr.employee", string="SalesPerson")
    product_id = fields.Many2one(
        "product.product",
        default=lambda self: self.env.ref(
            "nf_pos_salesperson_commission.nf_pos_commission_product",
            raise_if_not_found=False,
        ),
    )
    commission_amount = fields.Float(string="Amount", store=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirm"),
            ("paid", "Paid"),
            ("cancel", "Cancel"),
        ],
        default="draft",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        "res.currency",
        "Currency",
        related="company_id.currency_id",
        default=lambda self: self.env.user.company_id.currency_id.id,
    )
    expense_id = fields.Many2one("hr.expense")
    count_expence = fields.Integer(compute="_compute_Expence")

    @api.model_create_multi
    def create(self, vals_list):
        for create_new_commission_line in vals_list:
            if not create_new_commission_line.get("name", _("New")) == _("New"):
                create_new_commission_line["name"] = self.env[
                    "ir.sequence"
                ].next_by_code("pos.commission.line")
            else:
                create_new_commission_line["name"] = self.env[
                    "ir.sequence"
                ].next_by_code("pos.commission.line")

        return super(PosCommissionLine, self).create(vals_list)

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

    def commission_confirm(self):
        self.state = "confirm"

    def commission_create_expense(self):
        self.state = "paid"

        expense = self.env["hr.expense"].create(
            {
                "nf_pos_order_line_id": self.id,
                "name": self.name,
                "payment_mode": "company_account",
                "price_unit": self.commission_amount,
                "product_id": self.product_id.id,
                "total_amount_currency": self.commission_amount,
                "quantity": 1,
                "employee_id": self.employee_id.id,
                "company_id": self.employee_id.company_id.id,
                "currency_id": self.currency_id.id,
            }
        )

        self.expense_id = expense.id

    def nf_view_expense_order(self):
        if self.expense_id.id:
            return {
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "hr.expense",
                "res_id": self.expense_id.id,
                "target": "current",
            }

    @api.depends("expense_id")
    def _compute_Expence(self):
        self.count_expence = 0
        for record in self:
            hr_expense_count = self.env["hr.expense"].search_count(
                [("nf_pos_order_line_id", "=", record.id)]
            )
            record.count_expence = hr_expense_count
