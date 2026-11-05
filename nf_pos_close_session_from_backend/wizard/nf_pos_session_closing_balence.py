# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

from odoo import fields, models


class NfPosSessionClosingBalence(models.TransientModel):
    _name = "pos.session.closing.balence"
    _description = "Nf Pos Session Closing Balence"

    nf_pos_config = fields.Char(string="Name")
    nf_starting_balence = fields.Float(string="Starting Balence")
    nf_expected_balence = fields.Float(String="Expected Balence")
    nf_total_orders = fields.Integer(string="Total Orders")
    nf_cash_register_balance_end_real = fields.Float(string="Ending Balance")

    def nf_save_ending_balence(self):
        active_pos_session_id = self.env.context["active_id"]
        active_pos_session_record = self.env["pos.session"].search(
            [("id", "=", active_pos_session_id)]
        )

        if round(self.nf_expected_balence, 2) != round(
            self.nf_cash_register_balance_end_real, 2
        ):
            raise UserError(
                _(
                    "The Ending Balance does not match the Expected Balance. Please verify the cash amount before closing the POS session."
                )
            )
        active_pos_session_record.close_session_from_ui()
        # bank_payment_method_diffs = bank_payment_method_diffs or {}
        # for session in active_pos_session_record:
        #     if any(
        #         order.state == "draft"
        #         for order in active_pos_session_record.get_session_orders()
        #     ):
        #         raise UserError(
        #             _("You cannot close the POS when orders are still in draft")
        #         )
        #     if session.state == "closed":
        #         raise UserError(_("This session is already closed."))
        #     stop_at = active_pos_session_record.stop_at or fields.Datetime.now()
        #     session.write({"state": "closing_control", "stop_at": stop_at})
        #     if not session.config_id.cash_control:
        #         return session.action_pos_session_close(
        #             balancing_account, amount_to_balance, bank_payment_method_diffs
        #         )
        #     # If the session is in rescue, we only compute the payments in the cash register
        #     # It is not yet possible to close a rescue session through the front end, see `close_session_from_ui`
        #     if session.rescue and session.config_id.cash_control:
        #         default_cash_payment_method_id = (
        #             active_pos_session_record.payment_method_ids.filtered(
        #                 lambda pm: pm.type == "cash"
        #             )[0]
        #         )
        #         orders = active_pos_session_record._get_closed_orders()
        #         total_cash = (
        #             sum(
        #                 orders.payment_ids.filtered(
        #                     lambda p: p.payment_method_id
        #                     == default_cash_payment_method_id
        #                 ).mapped("amount")
        #             )
        #             + active_pos_session_record.cash_register_balance_start
        #         )

        #         session.cash_register_balance_end_real = total_cash
        #     active_pos_session_record.cash_register_balance_end_real = (
        #         self.nf_cash_register_balance_end_real
        #     )

        #     return session.action_pos_session_validate(
        #         balancing_account, amount_to_balance, bank_payment_method_diffs
        #     )
