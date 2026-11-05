/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { PurchaseOrderPopup } from "@nf_pos_purchase_order/js/PurchaseOrderPopup";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(ControlButtons.prototype, {
    setup() {
        super.setup(...arguments);
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.notification = useService("notification");
        this.create_po = this.pos.config.create_po;
    },

    async OnPurchaseOrderPopupClick() {
        let order = this.pos.getOrder();
        if (order.priceIncl <= 0 || order.lines.length == 0) {
            return this.dialog.add(ConfirmationDialog, {
                title: _t('Error'),
                body: _t('Cart is empty please select item which you want to purchase!'),
            })
        }

        await this.dialog.add(PurchaseOrderPopup, {
            order: order,
            po_status: this.pos.config.po_status,
            validate_po_receipt: this.pos.config.validate_po_receipt,
            create_bill: this.pos.config.create_bill,
        });
    },
});