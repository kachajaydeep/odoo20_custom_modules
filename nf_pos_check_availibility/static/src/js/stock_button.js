/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { proxy } from "@odoo/owl";

patch(ControlButtons.prototype, {
    setup() {
        super.setup(...arguments);
        this.stockCheckState = proxy({ loading: false });
    },

    async checkStock() {
        if (this.stockCheckState.loading) return;

        const order = this.pos.getOrder();
        if (!order || order.isEmpty()) return;

        this.stockCheckState.loading = true;

        try {
            for (const line of order.getOrderlines()) {
                try {
                    const result = await this.pos.data.call(
                        "stock.quant",
                        "nf_check_availibility",
                        [[], line.product_id.id]
                    );

                    const qty = result?.qty ?? 0;
                    line.nf_stock_availability = qty >= line.getQuantity();

                } catch (err) {
                    console.error(`Stock check failed for ${line.product_id.display_name}:`, err);
                    line.nf_stock_availability = undefined;
                }
            }
        } finally {
            this.stockCheckState.loading = false;
        }
    },
});