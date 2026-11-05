import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";

patch(PosStore.prototype, {
    async addLineToOrder(vals, order, opts = {}, configure = true) {
        const line = await super.addLineToOrder(...arguments);
        
        if(line.order_id.nf_discount_type == 'amount') { 
            return; 
        }

        if (!line) { return line; }
        if (order.nf_global_discoount) {
            line.setDiscount(
                parseFloat(order.nf_global_discoount.toFixed(2))
            );
        }
        return line;
    },
});

patch(PosOrder.prototype, {
    get get_nf_global_discount() {
        return this.nf_global_discoount || 0;
    },

    set_nf_global_discount(type, discount) {
        this.nf_discount_type = type;
        this.nf_global_discoount = discount;
    }
});

patch(PosOrderline.prototype, {
    setQuantity(quantity, keep_price) {
        const result = super.setQuantity(...arguments);
        const order = this.order_id;
        const original_price = this.displayPriceNoDiscount;
        const d = order.nf_global_discoount;
        const fixed_d = (d * original_price) / 100;
        // console.log("Original total = ",original_price,"Fixed Amount = ",fixed_d);

        let discount = (fixed_d * 100) / original_price;

        if(order.nf_discount_type == 'amount'){
            for (const line of order.lines) {
                line.setDiscount(discount / line.qty);
            }
        }
        return result;
    },
});