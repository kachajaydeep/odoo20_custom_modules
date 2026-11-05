/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { _t } from "@web/core/l10n/translation";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PosStore.prototype, {
    async pay() {
        const config = this.config;
        const order = this.getOrder();

        if (!order || order.isEmpty()) {
            return super.pay(...arguments);
        }

        if (!config.nf_check_stock) {
            return super.pay(...arguments);
        }

        if (config.nf_allow_to_sale) {
            return super.pay(...arguments);
        }

        const lines = order.getOrderlines();
        const notChecked = lines.some(
            (line) => line.nf_stock_availability === undefined
        );

        const hasUnavailable = lines.some(
            (line) => line.nf_stock_availability === false
        );
        if (hasUnavailable) {
            this.dialog.add(ConfirmationDialog, {
                title: _t("Stock Warning !"),
                body: _t("Stock is not available!"),
                confirmLabel: _t("OK"),
            });
            return;
        }
        return super.pay(...arguments);
    },
});