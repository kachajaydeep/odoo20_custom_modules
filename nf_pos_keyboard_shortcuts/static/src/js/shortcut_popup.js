import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { Dialog } from "@web/core/dialog/dialog";

const ACTION_LABELS = {
    back_action: "Back",
    product_screen: "Product Screen",
    payment_screen: "Payment Screen",
    ticket_screen: "Orders Screen",
    customer_screen: "Customer Screen",
    new_order: "New Order",
    delete_order: "Delete Order",
    duplicate_order: "Duplicate Order",
    validate_order: "Validate Order",
    next_order: "Next Order",
    prev_order: "Previous Order",
    next_orderline: "Next Order Line",
    prev_orderline: "Previous Order Line",
    save_order_later: "Save Order Later",
    numpad_qty: "Numpad Quantity",
    numpad_discount: "Numpad Discount",
    numpad_price: "Numpad Price",
    select_customer: "Select Customer",
    clear_customer: "Clear Customer",
    action_button: "Action Button",
    focus_search_bar: "Focus Search Bar",
    clear_search: "Clear Search",
    add_product_barcode: "Start/Stop Barcode Scanner",
    validate_payment: "Validate Payment",
    add_cash_payment: "Add Cash Payment",
    add_card_payment: "Add Card Payment",
    add_customer_account_payment: "Add Customer Account Payment",
    lock_pos: "Lock POS",
    logout_cashier: "Logout Cashier",
    close_session: "Close Session",
    open_register: "Open/Unlock Register",
    open_cash_drawer: "Cash In/Out",
    reload_data: "Reload Data",
    shortcuts_list: "Show Shortcuts",
    create_product: "Create Product",
    cashier_selection: "Cashier Selection",
};

export class ShortcutPopup extends Component {
    static template = "nf_pos_keyboard_shortcuts.ShortcutPopup";
    static components = { Dialog };
    static props = { close: Function };

    setup() {
        this.pos = usePos();
    }

    get shortcuts() {
        const raw = this.pos.config.nf_shortcut_ids || [];
        return raw
            .filter(sc => sc.nf_is_active === true)
            .map(sc => ({
                id: sc.id,
                nf_name: sc.nf_name,
                nf_key_combination: sc.nf_key_combination,
                nf_action: sc.nf_action,
                nf_sequence: sc.nf_sequence,
                nf_is_active: sc.nf_is_active,
                nf_action_label: ACTION_LABELS[sc.nf_action] || sc.nf_action,
                nf_description: sc.nf_description
            }))
            .sort((a, b) => (a.nf_sequence || 10) - (b.nf_sequence || 10));
    }
}