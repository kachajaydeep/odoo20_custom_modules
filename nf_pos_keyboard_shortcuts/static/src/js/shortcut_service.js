import { registry } from "@web/core/registry";
import { SyncPopup } from "@point_of_sale/app/components/popups/sync_popup/sync_popup";
import { _t } from "@web/core/l10n/translation";
import { ShortcutPopup } from "@nf_pos_keyboard_shortcuts/js/shortcut_popup";
import { ask } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { SelectionPopup } from "@point_of_sale/app/components/popups/selection_popup/selection_popup";

const SCREEN_RESTRICTIONS = {
    validate_payment: ["PaymentScreen"],
    add_cash_payment: ["ProductScreen", "PaymentScreen"],
    add_card_payment: ["ProductScreen", "PaymentScreen"],
    add_customer_account_payment: ["ProductScreen", "PaymentScreen"],
    focus_search_bar: ["ProductScreen"],
    clear_search: ["ProductScreen"],
    add_product_barcode: ["ProductScreen"],
    validate_order: ["ProductScreen"],
    select_customer: ["ProductScreen"],
    clear_customer: ["ProductScreen"],
    duplicate_order: ["ProductScreen"],
    delete_order: ["ProductScreen", "TicketScreen"],
    next_order: ["ProductScreen", "PaymentScreen", "TicketScreen"],
    prev_order: ["ProductScreen", "PaymentScreen", "TicketScreen"],
    next_orderline: ["ProductScreen"],
    prev_orderline: ["ProductScreen"],
    save_order_later: ["ProductScreen"],
    numpad_qty: ["ProductScreen"],
    numpad_price: ["ProductScreen"],
    numpad_discount: ["ProductScreen"],
    action_button: ["ProductScreen"],
    open_register: ["LoginScreen"],
};

export const shortcutService = {
    dependencies: ["dialog", "notification"],

    start(env, { dialog, notification }) {
        let pos = null;
        let shortcuts = [];
        let enabled = false;
        let lastFired = 0;
        const COOLDOWN = 300;

        function notify(message) {
            notification.add(message, {
                type: "info",
                duration: 1500,
            });
        }

        function normalizeKey(ev) {
            const parts = [];
            if (ev.ctrlKey) parts.push("CTRL");
            if (ev.shiftKey) parts.push("SHIFT");
            if (ev.altKey) parts.push("ALT");
            if (ev.metaKey) parts.push("META");
            const ignored = ["Control", "Shift", "Alt", "Meta"];
            if (!ignored.includes(ev.key)) {
                parts.push(ev.key.toUpperCase());
                // parts.push(ev.key);
            }
            return parts.join(" + ");
        }

        function isTypingContext() {
            const el = document.activeElement;
            const tag = el?.tagName;

            if (!["INPUT", "TEXTAREA", "SELECT"].includes(tag)) { return false; }
            if (el.closest(".numpad")) { return false; }
            return true;
        }

        function hasOpenDialog() {
            return !!document.querySelector(".modal.show, .o_dialog");
        }

        function currentScreen() {
            return pos?.router?.currentScreen();
        }


        function onKeyDown(ev) {

            if (!enabled || !shortcuts.length) { return; }
            if (isTypingContext()) { return; }
            if (hasOpenDialog()) return;

            const now = Date.now();
            if (ev.repeat || now - lastFired < COOLDOWN) return;

            if (ev.key === "Backspace" && !isTypingContext()) {
                ev.preventDefault();
                ACTION_HANDLERS.back_action?.(pos, dialog, notify);
                return;
            }

            const pressed = normalizeKey(ev);

            const match = shortcuts.find(sc => {
                return sc.nf_key_combination === pressed;
            });

            if (!match) return;

            const allowed = SCREEN_RESTRICTIONS[match.nf_action];
            if (allowed && !allowed.includes(currentScreen())) return;

            lastFired = now;

            ev.preventDefault();
            ev.stopPropagation();

            const handler = ACTION_HANDLERS[match.nf_action];
            if (handler && pos) {
                try {
                    handler(pos, dialog, notify);
                } catch (e) {
                    console.warn("[NF Shortcuts] Handler error:", e);
                }
            }
        }

        document.addEventListener("keydown", onKeyDown, true);

        return {
            register(posInstance) {
                pos = posInstance;
                enabled = pos.config.nf_enable_keyboard_shortcuts;
                if (!enabled) return;

                shortcuts = (pos.config.nf_shortcut_ids || [])
                    .filter(sc => sc.nf_is_active === true)
                    .map(sc => ({
                        nf_key_combination: sc.nf_key_combination,
                        nf_action: sc.nf_action,
                    }));
            },
            destroy() {
                document.removeEventListener("keydown", onKeyDown, true);
            },
        };
    },
};

const ACTION_HANDLERS = {

    back_action: (pos) => {
        // 1. Close popup/dialog first
        const closeBtn = document.querySelector(
            ".modal.show .btn-close, .o_dialog .btn-close"
        );

        if (closeBtn) {
            closeBtn.click();
            return;
        }

        // 2. Close popup via ESC button if exists
        const cancelBtn = document.querySelector(
            ".modal.show .btn-secondary, .popup-cancel"
        );
        if (cancelBtn) {
            cancelBtn.click();
            return;
        }

        // 3. Screen navigation
        const current = pos.router?.currentScreen();
        if (current === "PaymentScreen") {
            pos.navigate("ProductScreen", {
                orderUuid: pos.getOrder()?.uuid,
            });
            return;
        }
        if (current === "TicketScreen") {
            pos.navigate("ProductScreen", {
                orderUuid: pos.getOrder()?.uuid,
            });
            return;
        }
        if (current === "ReceiptScreen") {
            pos.navigate("ProductScreen", {
                orderUuid: pos.getOrder()?.uuid,
            });
            return;
        }
    },


    product_screen: (pos) => {
        pos.navigate("ProductScreen", { orderUuid: pos.getOrder()?.uuid });
    },
    payment_screen: (pos) => {
        if (pos.getOrder()?.canPay()) {
            pos.navigate("PaymentScreen", { orderUuid: pos.getOrder()?.uuid });
        }
    },
    ticket_screen: (pos) => {
        pos.navigate("TicketScreen");
    },
    customer_screen: (pos) => {
        pos.selectPartner();
    },


    new_order: (pos) => {
        const btn = document.querySelector(".list-plus-btn");
        if (btn) {
            btn.click();
        } else {
            pos.addNewOrder();
            pos.navigate("ProductScreen", { orderUuid: pos.getOrder()?.uuid });
        }
    },
    delete_order: async (pos) => {
        const order = pos.getOrder();
        if (!order) return;
        if (order.lines.length === 0) return;
        await pos.onDeleteOrder(order);
    },
    duplicate_order: (pos) => {
        const order = pos.getOrder();
        if (!order) return;
        const newOrder = pos.createNewOrder();
        for (const line of order.lines) {
            pos.data.models["pos.order.line"].create({
                order_id: newOrder,
                product_id: line.product_id,
                product_tmpl_id: line.product_tmpl_id,
                qty: line.qty,
                price_unit: line.price_unit,
                price_type: line.price_type,
                discount: line.discount,
                note: line.note,
                tax_ids: line.tax_ids?.map(t => ["link", t]) || [],
                attribute_value_ids: line.attribute_value_ids?.map(a => ["link", a]) || [],
            });
        }
        pos.setOrder(newOrder);
        pos.navigate("ProductScreen", { orderUuid: newOrder.uuid });
    },
    validate_order: (pos) => {
        const order = pos.getOrder();
        if (order?.canPay()) {
            pos.navigate("PaymentScreen", { orderUuid: order.uuid });
        }
    },
    next_order: (pos) => {
        const orders = pos.getOpenOrders();
        if (orders.length <= 1) return;
        const currentIndex = orders.findIndex(o => o.uuid === pos.selectedOrderUuid);
        const nextIndex = (currentIndex + 1) % orders.length;
        pos.setOrder(orders[nextIndex]);
        pos.navigate("ProductScreen", { orderUuid: orders[nextIndex].uuid });
    },

    prev_order: (pos) => {
        const orders = pos.getOpenOrders();
        if (orders.length <= 1) return;
        const currentIndex = orders.findIndex(o => o.uuid === pos.selectedOrderUuid);
        const prevIndex = (currentIndex - 1 + orders.length) % orders.length;
        pos.setOrder(orders[prevIndex]);
        pos.navigate("ProductScreen", { orderUuid: orders[prevIndex].uuid });
    },
    next_orderline: (pos) => {
        const order = pos.getOrder();
        if (!order) return;
        const lines = order.getOrderlines();
        if (lines.length <= 1) return;
        const currentIndex = lines.findIndex(l => l.uuid === order.getSelectedOrderline()?.uuid);
        const nextIndex = (currentIndex + 1) % lines.length;
        order.selectOrderline(lines[nextIndex]);
    },
    prev_orderline: (pos) => {
        const order = pos.getOrder();
        if (!order) return;
        const lines = order.getOrderlines();
        if (lines.length <= 1) return;
        const currentIndex = lines.findIndex(l => l.uuid === order.getSelectedOrderline()?.uuid);
        const prevIndex = (currentIndex - 1 + lines.length) % lines.length;
        order.selectOrderline(lines[prevIndex]);
    },
    save_order_later: (pos, _dialog, notify) => {
        const order = pos.getOrder();
        if (!order?.getOrderlines().length) {
            notify("No products in the order");
            return;
        }
        pos.clickSaveOrder();
    },


    select_customer: (pos) => {
        pos.selectPartner();
    },
    clear_customer: (pos, _dialog, notify) => {
        const order = pos.getOrder();
        if (order) {
            notify("Customer cleared");
            order.setPartner(null);
        }
    },


    focus_search_bar: () => {
        const el = document.querySelector(
            ".product-screen .input-group .o_input, " +
            ".pos-content .input-group .o_input, " +
            ".product-list .input-group .o_input"
        );
        if (el) {
            el.focus();
            el.select();
        } else {
            const all = document.querySelectorAll("input.o_input");
            for (const input of all) {
                if (input.offsetParent !== null) {
                    input.focus();
                    input.select();
                    break;
                }
            }
        }
    },
    clear_search: () => {
        const input = document.querySelector("input.o_input");
        if (!input) { return; }
        input.focus();
        input.value = "";
        input.dispatchEvent(new InputEvent("input", { bubbles: true, data: "", inputType: "deleteContentBackward", }));
    },
    add_product_barcode: () => {
        const btn = document.querySelector('button:has(i[data-icon="barcode"])');
        btn?.click();
    },


    validate_payment: (pos) => {
        if (pos.router?.currentScreen() !== "PaymentScreen") return;
        const btn = document.querySelector(
            ".payment-screen .btn-primary, .validation-button, .button.next"
        );
        btn?.click();
    },
    add_cash_payment: (pos) => {
        const order = pos.getOrder();
        if (!order?.canPay()) return;
        pos.navigate("PaymentScreen", { orderUuid: order.uuid });
        setTimeout(() => {
            const cashMethod = pos.models["pos.payment.method"]
                .getAll()
                .find(pm => pm.type === "cash");
            if (cashMethod) {
                document.querySelector(
                    `.payment-method-button[data-id="${cashMethod.id}"], .paymentmethod`
                )?.click();
            }
        }, 150);
    },
    add_card_payment: (pos) => {
        const order = pos.getOrder();
        if (!order?.canPay()) return;
        pos.navigate("PaymentScreen", { orderUuid: order.uuid });
        setTimeout(() => {
            const bankMethod = pos.models["pos.payment.method"]
                .getAll()
                .find(pm => pm.type === "bank");
            if (bankMethod) {
                const btn =
                    document.querySelector(`.payment-method-button[data-id="${bankMethod.id}"]`) ||
                    document.querySelector(`[data-payment-id="${bankMethod.id}"]`) ||
                    document.querySelectorAll(".paymentmethod")?.[1];
                btn?.click();
            }
        }, 150);
    },
    add_customer_account_payment: (pos) => {
        const order = pos.getOrder();
        if (!order?.canPay()) return;
        pos.navigate("PaymentScreen", { orderUuid: order.uuid });
        setTimeout(() => {
            const customerMethod = pos.models["pos.payment.method"]
                .getAll()
                .find(pm => pm.type === "pay_later");
            if (customerMethod) {
                const btn =
                    document.querySelector(`.payment-method-button[data-id="${customerMethod.id}"]`) ||
                    document.querySelector(`[data-payment-id="${customerMethod.id}"]`) ||
                    document.querySelectorAll(".paymentmethod")?.[2];
                btn?.click();
            }
        }, 150);
    },


    lock_pos: (pos) => {
        pos.showLoginScreen();
    },
    logout_cashier: (pos) => {
        pos.showLoginScreen();
    },
    close_session: async (pos) => {
        const confirmed = await ask(pos.env.services.dialog, {
            title: _t("Close Session"),
            body: _t("Are you sure you want to close the POS session?"),
        });
        if (confirmed) pos.closeSession();
    },
    open_cash_drawer: (pos, _dialog, notify) => {
        notify("Cash In/Out opened");
        pos.cashMove();
    },
    open_register: (pos, _dialog, notify) => {
        const btn = document.querySelector(".open-register-btn");
        if (!btn) {
            notify("Register is already open");
            return;
        }
        btn?.click();
    },


    reload_data: (pos, dialog) => {
        pos.env.services.dialog.add(SyncPopup, {
            title: _t("Reload Data"),
            confirm: (fullReload) => pos.reloadData(fullReload),
        });
    },
    shortcuts_list: (pos) => {
        pos.env.services.dialog.add(ShortcutPopup, {});
    },
    create_product: (pos) => {
        pos.editProduct();
    },
    cashier_selection: (pos) => {
        const btn = document.querySelector(
            ".cashier-name"
        );
        btn?.click();
    },


    numpad_qty: () => {
        document.querySelector(".numpad-qty")?.click();
    },
    numpad_price: (pos) => {
        document.querySelector(".numpad-price")?.click();
    },
    numpad_discount: () => {
        document.querySelector(".numpad-discount")?.click();
    },


    action_button: (pos) => {
        document.querySelector(".more-btn")?.click();
    },


};

registry.category("services").add("nf_pos_shortcut_service", shortcutService);