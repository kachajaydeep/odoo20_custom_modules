# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api, _
from datetime import datetime, timedelta, time


class NfCommissionReport(models.TransientModel):
    _name = "nf.commission.report"

    start_datetime = fields.Datetime(required=True)
    end_datetime = fields.Datetime(required=True)
    employee_id = fields.Many2one("hr.employee", required=True)

    def generate_commission_report(self):
        tz = self.env.context.get("tz")
        current_date = fields.Datetime.context_timestamp(
            self.with_context(tz=tz), timestamp=datetime.now()
        )
        start_time = fields.Datetime.context_timestamp(
            self.with_context(tz=tz), self.start_datetime
        )
        end_time = fields.Datetime.context_timestamp(
            self.with_context(tz=tz), self.end_datetime
        )

        pos_commission_line = self.env["pos.commission.line"].search(
            [("create_date", ">=", start_time), ("create_date", "<=", end_time)]
        )
        confirm_amount = 0
        draft_amount = 0
        paid_amount = 0
        cancel_amount = 0

        total_commission = 0
        order_data = []
        # if not pos_orders.session_id.config_id.apply_commission:
        #     return False

        for record in pos_commission_line:
            amount = round(record.commission_amount, 2)
            if (
                record
                and record.employee_id.id == self.employee_id.id
                and record.commission_amount != 0
            ):
                total_commission += round(amount, 2)
                order_data.append(
                    {
                        "date_order": (
                            record.create_date.strftime("%Y-%m-%d")
                            if record.create_date
                            else None
                        ),
                        "state": record.state,
                        "commission_amount": amount,
                        "order_name": record.name,
                    }
                )
                if (
                    record
                    and record.commission_amount != 0
                    and record.state == "confirm"
                ):
                    confirm_amount += amount

                if record and record.commission_amount != 0 and record.state == "draft":
                    draft_amount += amount

                if record and record.commission_amount != 0 and record.state == "paid":
                    paid_amount += amount

                if (
                    record
                    and record.commission_amount != 0
                    and record.state == "cancel"
                ):
                    cancel_amount += amount

        order_data.append(
            {
                "date_start": (
                    start_time.strftime("%d/%m/%Y %H:%M:%S") if start_time else None
                ),
                "date_stop": (
                    end_time.strftime("%d/%m/%Y %H:%M:%S") if end_time else None
                ),
                "employee_name": self.employee_id.name,
                "company_name": self.env.company.name,
                "current_date": current_date,
                "total_commission": total_commission,
                "confirm_amount": confirm_amount,
                "draft_amount": draft_amount,
                "paid_amount": paid_amount,
                "cancel_amount": cancel_amount,
            }
        )

        if total_commission == 0:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "type": "danger",
                    "message": _("Employee Must have Commission amount"),
                    "next": {"type": "ir.actions.act_window_close"},
                },
            }
        return self.env.ref(
            "nf_pos_salesperson_commission.nf_commission_report_action"
        ).report_action(None, data={"orders": order_data})
