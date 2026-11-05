/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { CashReceipt } from "@nf_pos_cash_control_receipts/app/screens/CashReceipt/CashReceipt";
import { CashReceiptPrintPopup } from "@nf_pos_cash_control_receipts/app/screens/CashReceiptPrintPopup/cashReceiptPrintPopup";

export class CashinOutScreen extends Component {
    static template = "nf_pos_cash_control_receipt.CashinOutScreen";
    static components = { CashReceipt };

    static props = {
        orderUuid: { type: String, optional: true },
        TotalCashData: { type: Array, optional: true },
        reason: { type: String, optional: true },
        date: { type: String, optional: true },
        amount: { type: String, optional: true },
        type: { type: String, optional: true },
    };

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
    }

    get currentOrder() {
        return this.pos.getOrder();
    }

    confirm() {
        this.pos.navigate("ProductScreen", {
            orderUuid: this.props.orderUuid,
        });
    }

    clickPrint() {
        // Build receiptProps — same shape CashReceipt expects
        const receiptProps = {
            order: this.currentOrder,
            sigle_receipt: this.props.TotalCashData === undefined,
            // single receipt fields
            reason: this.props.reason,
            date: this.props.date,
            amount: this.props.amount,
            type: this.props.type,
            // all receipts field
            TotalCashData: this.props.TotalCashData,
        };

        this.dialog.add(CashReceiptPrintPopup, {
            receiptProps,
        });
    }
}

registry.category("pos_pages").add("CashinOutScreen", {
    name: "CashinOutScreen",
    component: CashinOutScreen,
    route: `/pos/ui/${odoo.pos_config_id}/cash_receipt_screen/{string:orderUuid}`,
    params: {
        orderUuid: true,
        TotalCashData: true,
        reason: true,
        date: true,
        amount: true,
        type: true,
    },
});