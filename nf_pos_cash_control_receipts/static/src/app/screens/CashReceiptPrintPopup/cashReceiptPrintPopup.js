/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, useProps, t } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useTrackedAsync } from "@point_of_sale/app/hooks/hooks";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

export class CashReceiptPrintPopup extends Component {
    static template = "nf_pos_cash_control_receipt.CashReceiptPrintPopup";
    static components = { Dialog };

    props = useProps({
        receiptProps: t.object(),
        close: t.function(),
    });

    setup() {
        this.pos = usePos();
        this.ui = useService("ui");

        this.doPrint = useTrackedAsync(() => this._printReceipt());

        setTimeout(() => {
            this.doPrint.call();
        }, 100);
    }

    async _printReceipt() {
        try {
            const iframe = await this.pos.ticketPrinter.generateIframe(
                "nf_pos_cash_control_receipt.CashReceiptPrintPopup",
                this.props.receiptProps
            );

            const result = await this.pos.ticketPrinter.printWithFallback({
                iframe,
                webFallback: true,
            });

            return result;
        } catch (error) {
            console.error("PRINT ERROR:", error);
            console.error("PRINT ERROR STACK:", error?.stack);
            throw error;
        }
    }

    get printList() {
        return [{
                label: _t("Cash Receipt"),
                method: () => this.doPrint.call(),
                status: this.doPrint.status,
                icon: "print",
                isPrimary: true,
            },
        ];
    }

    clickPrintButton(item) {
        item.method();
    }
}