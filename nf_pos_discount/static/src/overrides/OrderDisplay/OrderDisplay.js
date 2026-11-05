import { OrderDisplay } from "@point_of_sale/app/components/order_display/order_display";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

patch(OrderDisplay.prototype, {
    setup() {
        super.setup(...arguments);
        this.pos = usePos();
    },

    get nfTotalDiscount() {
        const order = this.pos.getOrder();
        if (!order) return 0;

        const lines = order.getOrderlines();
        if (!lines.length) return 0;

        const total = lines.reduce((sum, line) => {
            if (line.discount) {
                return sum + (line.displayPriceNoDiscount * line.discount) / 100;
            }
            return sum;
        }, 0);
        
        // console.log("Total Discount to show", total);
        return total || 0;
    },
});