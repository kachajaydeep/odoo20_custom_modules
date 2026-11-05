import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { OrderDisplay } from "@point_of_sale/app/components/order_display/order_display";

patch(OrderDisplay.prototype, {
    setup(){
        super.setup(...arguments)
        this.pos = usePos()
    },

    get totalWeight() {
        const order = this.pos.getOrder();
        if (!order) return "0.000";
        const total = order.getOrderlines().reduce((sum, line) => {
            return sum + (line.product_id?.weight || 0) * line.getQuantity();
        }, 0);
        return total.toFixed(3);
    },

    get totalVolume() {
        const order = this.pos.getOrder();
        if (!order) return "0.000";
        const total = order.getOrderlines().reduce((sum, line) => {
            return sum + (line.product_id?.volume || 0) * line.getQuantity();
        }, 0);
        return total.toFixed(3);
    },
});
