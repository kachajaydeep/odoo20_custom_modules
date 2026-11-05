import { SelectPartnerButton } from "@point_of_sale/app/screens/product_screen/control_buttons/select_partner_button/select_partner_button";
import { patch } from "@web/core/utils/patch";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { OrderTypes } from "@nf_pos_order_type/apps/order_type_popup/order_types_popup";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

patch(SelectPartnerButton.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
        this.dialog = useService("dialog");
    },

    async onClickOrderType() {
        const payload = await makeAwaitable(
            this.dialog,
            OrderTypes,
            {}
        );
    },
});