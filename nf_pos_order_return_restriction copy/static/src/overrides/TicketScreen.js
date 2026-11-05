/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(TicketScreen.prototype, {
    onClickOrder(clickedOrder) {
        if (this.pos.config.nf_restrict_return_order){
            if (clickedOrder.return_exprired){
                this.dialog.add(AlertDialog, {
                    title: _t("Return Policy Expired !"),
                    body: _t("You are not allow to return the order. Order return policy expired")
                });
            }else{
                super.onClickOrder(...arguments)
            }
        }else{
            super.onClickOrder(...arguments)
        }
    }
})