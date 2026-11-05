/** @odoo-module */

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { useService } from "@web/core/utils/hooks";
import { useAsyncLockedMethod } from "@point_of_sale/app/utils/hooks";

export class NfStockButton extends Component {
    static template = "nf_pos_check_availibility.NfStockButton";

    setup() {
        this.pos = usePos();
        this.click = useAsyncLockedMethod(this.click);
        this.orm = useService("orm");
    }

    _isDisabled() {
        const order = this.pos.get_order();
        if (!order) {
            return false;
        }
        return order.get_orderlines().length === 0;
    }

    async click() {
        const orderlines = this.pos.get_order().get_orderlines()
        for (let i=0; i <  orderlines.length; i++){
            const line = orderlines[i]
            const stock = await this.orm.call("stock.quant", "nf_check_availibility", [[], line.product.id]);
            if (stock){
                line.stock_availibility = true
            }else{
                line.stock_availibility = false
            }
        }
    }
}

ProductScreen.addControlButton({
    component: NfStockButton,
    condition: function () {
        return this.pos.config.nf_check_stock;
    },
});
