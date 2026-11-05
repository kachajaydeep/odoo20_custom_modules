/** @odoo-module */
import { ProductInfoPopup } from "@point_of_sale/app/screens/product_screen/product_info_popup/product_info_popup";
import { patch } from "@web/core/utils/patch";

patch(ProductInfoPopup.prototype, {
    setup() {
        super.setup();
    },
    get getNfStock() {
        var self = this;
        let stocks = this.pos.models['stock.quant'].filter((x) => x.product_id?.id == self.props.product.id);
        if (stocks && stocks.length) { return stocks } 
        else { return false; }
    },
    get_width(name) {
        if (name && name.length < 20) { return "width_25"; } 
        else if (name && name.length < 40) { return "width_35"; } 
        else { return "width_50"; }
    },
});