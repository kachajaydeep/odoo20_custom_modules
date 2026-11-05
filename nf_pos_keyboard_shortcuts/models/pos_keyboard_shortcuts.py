# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, api, fields #type: ignore
from odoo.exceptions import ValidationError #type: ignore

class PosKeyboardShortcut(models.Model):
    _name = "pos.keyboard.shortcut"
    _description = "POS Keyboard Shortcut"
    _order = "nf_sequence, id"

    nf_sequence = fields.Integer(default=10,string="Sequence")
    nf_is_active = fields.Boolean(
        string="Is active",
        default=True,
        help="Enable or disable this shortcut."
    )
    nf_name = fields.Char(
        string="Name",
        required=True,
        help="Shortcut name."
    )
    nf_key_combination = fields.Char(
        string="Shortcut Key",
        required=True,
        help="Example: F8, CTRL+ENTER, CTRL+N"
    )
    nf_action = fields.Selection(
        [   
            ("back_action", "Back"),
            
            # Navigation
            ("product_screen", "Product Screen"),
            ("payment_screen", "Payment Screen"),
            ("ticket_screen", "Orders Screen"),
            ("customer_screen", "Customer Screen"),

            # Orders
            ("new_order", "New Order"),
            ("delete_order", "Delete Order"),
            ("duplicate_order", "Duplicate Order"),
            ("validate_order", "Validate Order"),
            ("next_order", "Next Order"),
            ("prev_order", "Previous Order"),
            ("next_orderline", "Next Order Line"),
            ("prev_orderline", "Previous Order Line"),
            ("save_order_later", "Save Order Later"),
            
            # Numpad
            ("numpad_qty", "Numpad Quantity"),
            ("numpad_discount", "Numpad Discount"),
            ("numpad_price", "Numpad Price"),

            # Customer
            ("select_customer", "Select Customer"),
            ("clear_customer", "Clear Customer"),
            
            # Action Button 
            ("action_button", "Action Button"),

            # Search
            ("focus_search_bar", "Focus Search Bar"),
            ("clear_search", "Clear Search"),
            ("add_product_barcode", "Start/Stop Barcode Scanner"),

            # Payments
            ("validate_payment", "Validate Payment"),
            ("add_cash_payment", "Add Cash Payment"),
            ("add_card_payment", "Add Card Payment"),
            ("add_customer_account_payment", "Add Customer Account Payment"),

            # Session
            ("lock_pos", "Lock POS"),
            ("logout_cashier", "Logout Cashier"),
            ("close_session", "Close Session"),
            ("open_register", "Open/Unlock Register"),
            ("open_cash_drawer", "Cash In/Out"),

            # Utilities
            ("reload_data", "Reload Data"),
            ("shortcuts_list", "Show Shortcuts"),
            ("create_product", "Create Product"),
            ("cashier_selection", "Cashier Selection"),
        ],
        required=True,
        string="Actions"
    )

    nf_description = fields.Text(help="Optional description of the shortcut.",string="Description")
    pos_config_id = fields.Many2one(
        "pos.config",
        required=True,
        ondelete="cascade",
    )
    
    @api.model
    def _load_pos_data_domain(self,data,config):
        return [
            ("pos_config_id", "=", config.id),
            ("nf_is_active", "=", True),
        ]
    
    @api.model
    def _load_pos_data_fields(self, config_id):
        return [
            "id",
            "nf_name",
            "nf_key_combination",
            "nf_action",
            "nf_description",
            "nf_sequence",
            "nf_is_active",
            "pos_config_id",
        ]
        
    @api.model
    def _load_pos_data_search_read(self,records,config):
        domain = self._load_pos_data_domain(records,config)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain,fields)
        return records

    def _get_action_label(self, action_key):
        return dict(self._fields["nf_action"].selection).get(action_key, action_key)

    def _find_duplicate_key(self, exclude_id=False):
        domain = [
            ("pos_config_id", "=", self.pos_config_id.id),
            ("nf_key_combination", "=", self.nf_key_combination),
            ("nf_is_active", "=", True),
        ]
        if exclude_id:
            domain.append(("id", "!=", exclude_id))
        return self.search(domain, limit=1)

    def _find_duplicate_action(self, exclude_id=False):
        domain = [
            ("pos_config_id", "=", self.pos_config_id.id),
            ("nf_action", "=", self.nf_action),
            ("nf_is_active", "=", True),
        ]
        if exclude_id:
            domain.append(("id", "!=", exclude_id))
        return self.search(domain, limit=1)
    
    
    @api.constrains("nf_key_combination", "nf_action", "nf_is_active", "pos_config_id")
    def _check_duplicates(self):
        for rec in self:
            if not rec.nf_is_active or not rec.pos_config_id:
                continue

            dup_key = self.search([
                ("id", "!=", rec.id),
                ("pos_config_id", "=", rec.pos_config_id.id),
                ("nf_key_combination", "=", rec.nf_key_combination),
                ("nf_is_active", "=", True),
            ], limit=1)

            if dup_key:
                raise ValidationError(
                    f"Shortcut key '{rec.nf_key_combination}' is already assigned to another shortcut."
                )

            dup_action = self.search([
                ("id", "!=", rec.id),
                ("pos_config_id", "=", rec.pos_config_id.id),
                ("nf_action", "=", rec.nf_action),
                ("nf_is_active", "=", True),
            ], limit=1)

            if dup_action:
                raise ValidationError(
                    f"Action '{self._get_action_label(rec.nf_action)}' is already assigned to another shortcut."
                )
                
            
    @api.onchange("nf_key_combination")
    def _onchange_nf_key_combination(self):
        if not self.nf_key_combination or not self.pos_config_id.id:
            return
        dup = self._find_duplicate_key(exclude_id=self._origin.id)
        if dup:
            return {"warning": {
                "title": "Duplicate Shortcut Key",
                "message": f"Shortcut key '{self.nf_key_combination}' is already assigned to another shortcut.",
            }}

    @api.onchange("nf_action")
    def _onchange_nf_action(self):
        if not self.nf_action or not self.pos_config_id.id:
            return
        dup = self._find_duplicate_action(exclude_id=self._origin.id)
        if dup:
            return {"warning": {
                "title": "Duplicate Action",
                "message": f"Action '{self._get_action_label(self.nf_action)}' is already assigned to another shortcut.",
            }}