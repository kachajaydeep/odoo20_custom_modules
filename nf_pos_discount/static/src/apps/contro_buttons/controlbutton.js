import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { NumberPopup } from "@point_of_sale/app/components/popups/number_popup/number_popup";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { _t } from "@web/core/l10n/translation";

patch(ControlButtons.prototype, {
    async GlobalDiscount() {
        const order = this.pos.getOrder();
        if (!order) return;

        const payload = await makeAwaitable(this.dialog, NumberPopup, {
            title: _t("Discount"),
            startingValue: 1,
            isInputSelected: true,
            is_custom_discount: true,
        });

        if (!payload) return;

        const lines = order.getOrderlines();
        let percentage;

        if (payload.discount_type === "amount") {
            for (const line of lines) {
                percentage = ((payload.amount / order.displayPrice) * 100) / line.qty;
            }
            
        } else {
            percentage = Math.max(0, Math.min(100, parseFloat(payload)));
        }
        order.set_nf_global_discount(payload.discount_type, percentage);

        for (const line of lines) {
            await line.setDiscount(parseFloat(percentage.toFixed(2)));
        }
    },

    async removeDiscount() {
        const order = this.pos.getOrder();
        if (!order) return;
        for (const line of order.getOrderlines()) {
            await line.setDiscount(0);
        }
    },
});