import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";


patch(ControlButtons.prototype, {
    order_list() {
        this.pos.navigate("NfOrderListScreen", {
            orderUuid: this.pos.selectedOrderUuid,
        });
        // this.pos.showScreen('NfOrderListScreen')
        // const order = this.pos.get_order();
        // const partner = order.get_partner();
        // const searchDetails = partner ? { fieldName: "PARTNER", searchTerm: partner.name } : {};
        // this.pos.showScreen("NfOrderListScreen", {
        //     ui: { filter: "SYNCED", searchDetails },
        //     destinationOrder: order,
        // });
    }
})