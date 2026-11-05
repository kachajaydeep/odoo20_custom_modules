import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { NfOrderListScreen } from "@nf_pos_order_list/screens/order_list/order_list";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons.prototype, {
    order_list() {
        this.pos.navigate("NfOrderListScreen"); 
    }
})