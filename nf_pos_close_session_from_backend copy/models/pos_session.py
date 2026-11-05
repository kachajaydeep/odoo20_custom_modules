# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError


class PosSession(models.Model):
    _inherit = "pos.session"

    def action_nf_pos_session_closing_control(self):
        cash_amount_total = 0.0
        for pos_order_record in self.order_ids:
            for cash_payment_record in pos_order_record.payment_ids:
                if cash_payment_record.payment_method_id.type == "cash":
                    cash_amount_total += cash_payment_record.amount

        session_data = {
            "nf_pos_config": self.name,
            "nf_starting_balence": self.opening_balance,
            "nf_expected_balence": self.opening_balance + cash_amount_total,
            "nf_total_orders": len(self.order_ids),
        }

        return {
            "type": "ir.actions.act_window",
            "name": "Closing Pos Session",
            "res_model": "pos.session.closing.balence",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_nf_pos_config": session_data["nf_pos_config"],
                "default_nf_starting_balence": session_data["nf_starting_balence"],
                "default_nf_expected_balence": session_data["nf_expected_balence"],
                "default_nf_total_orders": session_data["nf_total_orders"],
            },
        }
