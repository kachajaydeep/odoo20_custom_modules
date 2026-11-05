/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { FeedbackScreen } from "@point_of_sale/app/screens/feedback_screen/feedback_screen";
import { PrintPopup } from "@point_of_sale/app/components/popups/print_popup/print_popup";

patch(FeedbackScreen.prototype, {
    async clickPrint() {
        const config = this.pos.config;
        const copyCount = config.nf_copy_count || 1;

        if (!config.nf_enbale_2x_print || copyCount <= 1) {
            return super.clickPrint();
        }

        this.stopAutomaticSkip();

        const order = this.currentOrder;

        for (let i = 0; i < copyCount; i++) {
            await new Promise((resolve) => {
                this.dialog.add(PrintPopup, {
                    order,
                    onClose: resolve,
                });
            });
        }
    },

    async _afterWaitFinished() {
        await super._afterWaitFinished();

        const config = this.pos.config;
        const copyCount = config.nf_copy_count || 1;

        if (
            !config.nf_enbale_2x_print ||
            !config.autoPrint ||
            copyCount <= 1
        ) {
            return;
        }

        const order = this.currentOrder;

        for (let i = 0; i < copyCount - 1; i++) {
            await new Promise((resolve) => setTimeout(resolve, 1000));
            await this.pos.ticketPrinter.printOrderReceipt({
                order,
                webFallback: true,
            });
        }
    },
});