/** @odoo-module **/

import { Component } from "@odoo/owl";
import { omit } from "@web/core/utils/objects";

export class CashReceipt extends Component {
    static template = "nf_pos_cash_control_receipt.CashReceipt";

    static props = {
        orderUuid: { type: String, optional: true },
        TotalCashData: { type: Object, optional: true },
        reason: { type: String, optional: true },
        date: { type: String, optional: true },
        amount: { type: String, optional: true },
        type: { type: String, optional: true },
        sigle_receipt: { type: Boolean, optional: true },
        order: { type: Object, optional: true },
    };

    omit(...args) {
        return omit(...args);
    }
}