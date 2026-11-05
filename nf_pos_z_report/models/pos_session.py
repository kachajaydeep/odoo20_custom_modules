# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models
from datetime import datetime, timedelta, time


class PosSession(models.Model):
    _inherit = "pos.session"

    def action_view_pos_z_report(self, data=None):
        tz = self.env.context.get("tz")
        current_date = fields.Datetime.context_timestamp(
            self.with_context(tz=tz), timestamp=datetime.now()
        )
        payment_methods = {}
        product_details = {}
        discount = 0
        amount_total = 0
        amount_tax = 0
        amount_unit_price = 0
        quantity = 0
        amount_discount = 0
        payment_type_list = []
        product_type_list = []
        payment_type_amount = 0
        without_tax_amount = 0

        for order_record in self.order_ids:
            amount_total += order_record.amount_total
            amount_tax += order_record.amount_tax

            for line_record in order_record.lines:
                quantity = line_record.qty
                discount = line_record.discount
                amount_unit_price = line_record.price_unit
                without_tax_amount += line_record.price_subtotal

                product_id = line_record.product_id.id

                if product_id not in product_type_list:
                    product_type_list.append(product_id)
                    product_details[product_id] = {
                        "product_name": line_record.product_id.name,
                        "product_quantity": line_record.qty,
                        "product_amount": line_record.price_subtotal_incl,
                    }
                else:
                    product_details[product_id]["product_quantity"] += line_record.qty
                    product_details[product_id][
                        "product_amount"
                    ] += line_record.price_subtotal_incl

                if discount and amount_unit_price and quantity:
                    amount_discount += (amount_unit_price * discount * quantity) / 100

            for payment_record in order_record.payment_ids:
                payment_id = payment_record.payment_method_id.id
                if payment_id not in payment_type_list:
                    payment_type_list.append(payment_id)
                    payment_type_amount = round(payment_record.amount, 2)
                    payment_methods[payment_id] = {
                        "payment_type": payment_record.payment_method_id.name,
                        "amount_payment": payment_type_amount,
                    }
                else:
                    payment_type_amount = round(payment_record.amount, 2)
                    payment_methods[payment_id]["amount_payment"] += payment_type_amount
                    payment_methods[payment_id]["amount_payment"] = round(
                        payment_methods[payment_id]["amount_payment"], 2
                    )

        current_order = {
            "current_date": current_date,
            "sales": round(amount_total, 2),
            "all_taxes": round(amount_tax, 2),
            "company_name": self.company_id.name,
            "company_website": self.company_id.website,
            "amount_discount": round(amount_discount, 2),
            "start_date": (
                self.start_at.strftime("%Y-%m-%d %H:%M:%S") if self.start_at else None
            ),
            "end_date": (
                self.stop_at.strftime("%Y-%m-%d %H:%M:%S") if self.stop_at else None
            ),
            "sales_without_tax": round(without_tax_amount, 2),
            "gross_total": round(without_tax_amount + amount_tax + amount_discount, 2),
        }
        return self.env.ref("nf_pos_z_report.z_reports_details_menu").report_action(
            self.ids,
            {
                "session_ids": self.ids,
                "current_order": current_order,
                "payment_methods": payment_methods,
                "product_details": product_details,
            },
        )
