# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields #type: ignore

class PosConfig(models.Model):
    _inherit = "pos.config"

    nf_enable_keyboard_shortcuts = fields.Boolean(
        string="Enable Keyboard Shortcuts",
        default=False,
        help="Enable keyboard shortcuts in the POS.",
    )
    
    nf_shortcut_ids = fields.One2many(
        "pos.keyboard.shortcut",
        "pos_config_id",
        string="Keyboard Shortcuts",
    )
    
    nf_shortcuts_pending_save = fields.Boolean(
        compute="_compute_shortcuts_pending_save",
    )

    def _compute_shortcuts_pending_save(self):
        for rec in self:
            rec.nf_shortcuts_pending_save = (
                rec.nf_enable_keyboard_shortcuts and not rec.nf_shortcut_ids
            )
    
    def _get_default_shortcuts(self):
        return [
            {"nf_name": "Back Action","nf_key_combination": "ARROWLEFT","nf_action": "back_action","nf_sequence": 10,"nf_description":"Return to the previous screen"},
            {"nf_name": "Product Screen","nf_key_combination": "F1","nf_action": "product_screen","nf_sequence": 20,"nf_description":"Open the product screen."},
            {"nf_name": "Payment Screen","nf_key_combination": "F2","nf_action": "payment_screen","nf_sequence": 30,"nf_description":"Navigate to the payment screen for checkout."},
            {"nf_name": "Orders Screen","nf_key_combination": "F3","nf_action": "ticket_screen","nf_sequence": 40,"nf_description":"View and manage open and completed orders."},
            {"nf_name": "Next Order","nf_key_combination": "SHIFT + ARROWDOWN","nf_action": "next_order","nf_sequence": 50,"nf_description":"Switch to the next active order."},
            {"nf_name": "Previous Order","nf_key_combination": "SHIFT + ARROWUP","nf_action": "prev_order","nf_sequence": 60,"nf_description":"Switch to the previous active order."},
            {"nf_name": "Next Order Line","nf_key_combination": "CTRL + ARROWDOWN","nf_action": "next_orderline","nf_sequence": 70,"nf_description":"Move the selection to the next order line."},
            {"nf_name": "Previous Order Line","nf_key_combination": "CTRL + ARROWUP","nf_action": "prev_orderline","nf_sequence": 80,"nf_description":"Move the selection to the previous order line."},
            {"nf_name": "Focus Search Bar","nf_key_combination": "CTRL + F","nf_action": "focus_search_bar","nf_sequence": 90,"nf_description":"Place the cursor in the product search field."},
            {"nf_name": "Clear Search","nf_key_combination": "CTRL + D","nf_action": "clear_search","nf_sequence": 100,"nf_description":"Clear the current search text and reset the product list."},
            {"nf_name": "Numpad Quantity","nf_key_combination": "Q","nf_action": "numpad_qty","nf_sequence": 110,"nf_description":"Add numpad quantity"},
            {"nf_name": "Numpad Discount","nf_key_combination": "D","nf_action": "numpad_discount","nf_sequence": 120,"nf_description":"Add numpad discount"},
            {"nf_name": "Numpad Price","nf_key_combination": "P","nf_action": "numpad_price","nf_sequence": 130,"nf_description":"Add numpad price"},
            {"nf_name": "Action Button","nf_key_combination": "SHIFT + A","nf_action": "action_button","nf_sequence": 140,"nf_description":"Open the actions menu"},
            {"nf_name": "Validate Order","nf_key_combination": "SHIFT + V","nf_action": "validate_order","nf_sequence": 150,"nf_description":"Validate current order"},
            {"nf_name": "Add Cash Payment","nf_key_combination": "ALT + C","nf_action": "add_cash_payment","nf_sequence": 160,"nf_description":"Add a cash payment to the current order."},
            {"nf_name": "Add Card Payment","nf_key_combination": "ALT + O","nf_action": "add_card_payment","nf_sequence": 170,"nf_description":"Add a card payment to the current order."},
            {"nf_name": "Add Customer Account Payment","nf_key_combination": "ALT + A","nf_action": "add_customer_account_payment","nf_sequence": 180,"nf_description":"Add payment using the customer's account balance."},
            {"nf_name": "Validate Payment","nf_key_combination": "SHIFT + ENTER","nf_action": "validate_payment","nf_sequence": 190,"nf_description":"Confirm the payment and complete the order."},
            {"nf_name": "Show Shortcuts","nf_key_combination": "F4","nf_action": "shortcuts_list","nf_sequence": 200,"nf_description":"Display the keyboard shortcuts reference."}
        ]

    def _create_default_shortcuts(self):
        for config in self:
            # Skip if shortcuts already exist
            if config.nf_shortcut_ids:
                continue
            defaults = config._get_default_shortcuts()
            for shortcut in defaults:
                self.env["pos.keyboard.shortcut"].create({
                    **shortcut,
                    "pos_config_id": config.id,
                    "nf_is_active": True,
                })

    def write(self, vals):
        res = super().write(vals)
        # When shortcuts are enabled and none exist yet, create defaults
        if vals.get("nf_enable_keyboard_shortcuts"):
            self._create_default_shortcuts()
        return res

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result.append("pos.keyboard.shortcut")
        return result