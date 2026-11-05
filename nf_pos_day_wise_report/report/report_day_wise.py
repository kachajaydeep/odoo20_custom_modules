# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author: Part of NextFlowIT.

from datetime import datetime, timedelta

import pytz

from odoo import api, fields, models


class ReportDayWise(models.AbstractModel):
    _name = "report.nf_pos_day_wise_report.nf_day_wise_doc"
    _description = "POS Day Wise Report"

    def _get_order_lines(self, orders):
        """Prepare POS order lines for the report."""
        result = []

        for order in orders:
            for line in order.lines:
                result.append({
                    "order_number": order.name,
                    "order_date": order.date_order,
                    "product_name": line.full_product_name,
                    "price": line.price_unit,
                    "qty": line.qty,
                    "subtotal": line.price_subtotal_incl,
                    "purchase_currency_id": order.currency_id.id,
                })

        return result

    def _get_orders_by_person(self, date_start, date_end, model, person_ids=None):
        """Return report data grouped by user/employee."""
        result = {}

        persons = self.env[model].sudo().search(
            [("id", "in", person_ids)] if person_ids else []
        )

        if not person_ids:
            persons = self.env[model].sudo().search([])

        field_name = "user_id" if model == "res.users" else "employee_id"

        for person in persons:
            domain = [
                ("date_order", ">=", date_start),
                ("date_order", "<", date_end),
                (field_name, "!=", False),
                (field_name, "=", person.id),
            ]

            orders = self.env["pos.order"].sudo().search(domain)

            result[person.display_name] = self._get_order_lines(orders)

        return result

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})

        report_date = fields.Date.from_string(data.get("date"))

        # Use user's timezone for day-wise reporting
        user_tz = pytz.timezone(
            self.env.context.get("tz")
            or self.env.user.tz
            or "UTC"
        )

        local_start = user_tz.localize(
            datetime.combine(report_date, datetime.min.time())
        )
        local_end = local_start + timedelta(days=1)

        date_start = local_start.astimezone(pytz.UTC).replace(tzinfo=None)
        date_end = local_end.astimezone(pytz.UTC).replace(tzinfo=None)

        order_dic_by_orders = {}
        order_dic_by_orders_hr = {}

        if data.get("pos_hr_installed"):
            order_dic_by_orders_hr = self._get_orders_by_person(
                date_start,
                date_end,
                "hr.employee",
                data.get("employee_ids"),
            )
        else:
            order_dic_by_orders = self._get_orders_by_person(
                date_start,
                date_end,
                "res.users",
                data.get("user_ids"),
            )

        data.update({
            "date_start": data.get("date"),
            "order_dic_by_orders": order_dic_by_orders,
            "order_dic_by_orders_hr": order_dic_by_orders_hr,
        })

        return data