/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { NfCustomReceipt } from "./nf_custom_receipt";
import { formatCurrency } from "@web/core/currency";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

patch(OrderReceipt, {
    setup() {
        this.pos = usePos();
        super.setup(...arguments);
    }
});
OrderReceipt.components = {
    ...OrderReceipt.components,
    NfCustomReceipt,
};
