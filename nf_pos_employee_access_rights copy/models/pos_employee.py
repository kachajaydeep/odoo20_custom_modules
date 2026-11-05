# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    nf_hide_payment_button = fields.Boolean(string="Hide Payment Button")
    nf_restrict_payment_method = fields.Boolean(string="Restrict Payment Method")
    nf_pos_payment_methods = fields.Many2many(
        "pos.payment.method",
        "nf_empl_restrict_payment_method",
        string="Payment methods",
    )
    nf_hide_customer_button = fields.Boolean(string="Hide Customer Button")
    nf_hide_info_button = fields.Boolean(string="Hide Info Button")
    nf_hide_cancel_order_button = fields.Boolean(string="Hide Cancel Order Button")
    nf_hide_payment_tip_button = fields.Boolean(string="Hide Payment Tip Button")
    nf_hide_payment_ship_later_button = fields.Boolean(string="Hide Ship Later Button")
    nf_hide_create_customer_button = fields.Boolean(
        string="Hide Create Customer Button"
    )
    nf_hide_delete_order_button = fields.Boolean(string="Hide Delete Order Button")
    nf_only_show_active_order = fields.Boolean(string="Only Show Active Orders")
    nf_hide_customer_note_button = fields.Boolean(string="Hide Customer Note Button")
    nf_disable_price_button = fields.Boolean(string="Disable Price Button")
    nf_hide_numpad_buttons = fields.Boolean(string="Hide Numpad Buttons")
    nf_hide_fiscal_button = fields.Boolean(string="Hide Fiscal Button")
    nf_hide_refund_button = fields.Boolean(string="Hide Refund Button")
    nf_hide_payment_validate_button = fields.Boolean(
        string="Hide Payment Validate Button"
    )
    nf_hide_quotation_button = fields.Boolean(string="Hide Quotation Button")
    nf_disable_discount_button = fields.Boolean(string="Disable Discount Button")
    nf_hide_pricelist_button = fields.Boolean(string="Hide Pricelist Button")
    nf_hide_close_pos_button = fields.Boolean(string="Hide Close POS Button")
    nf_hide_backend_pos_button = fields.Boolean(string="Hide Backend POS Button")
    nf_disable_plus_minus_button = fields.Boolean(string="Disable (+/-) Button")
    nf_hide_pos_categories = fields.Boolean(string="Hide POS Categories")
    nf_disable_qty_button = fields.Boolean(string="Disable Quantity Button")
    nf_hide_payment_invoice_button = fields.Boolean(
        string="Hide Payment Invoice Button"
    )
    nf_hide_debug_window = fields.Boolean(string="Hide Debug Window")
    nf_hide_cash_in_out_pos_button = fields.Boolean(
        string="Hide Cash In/Out POS Button"
    )

    @api.onchange("nf_only_show_active_order")
    def _onchange_nf_only_show_active_order(self):
        if self.nf_only_show_active_order:
            self.nf_hide_refund_button = True
        else:
            self.nf_only_show_active_order = False

    @api.model
    def _load_pos_data_fields(self, config):
        result = super()._load_pos_data_fields(config)

        result += [
            "nf_hide_payment_button",
            "nf_pos_payment_methods",
            "nf_restrict_payment_method",
            "nf_hide_customer_button",
            "nf_hide_info_button",
            "nf_hide_cancel_order_button",
            "nf_hide_payment_tip_button",
            "nf_hide_payment_ship_later_button",
            "nf_hide_create_customer_button",
            "nf_hide_delete_order_button",
            "nf_only_show_active_order",
            "nf_hide_customer_note_button",
            "nf_disable_price_button",
            "nf_hide_numpad_buttons",
            "nf_hide_fiscal_button",
            "nf_hide_refund_button",
            "nf_hide_payment_validate_button",
            "nf_hide_quotation_button",
            "nf_disable_discount_button",
            "nf_hide_pricelist_button",
            "nf_hide_close_pos_button",
            "nf_hide_backend_pos_button",
            "nf_disable_plus_minus_button",
            "nf_hide_pos_categories",
            "nf_disable_qty_button",
            "nf_hide_payment_invoice_button",
            "nf_hide_debug_window",
            "nf_hide_cash_in_out_pos_button",
        ]

        return result
