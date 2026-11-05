import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {  
    async validateOrder(args = {}) {
        const order = this.getOrder();
        const lines = order.getOrderlines();
        const totalWeight = lines.reduce((sum,line) => {
            return sum + (line.product_id?.weight || 0) * line.getQuantity()
        },0);

        let totalVolume = lines.reduce((sum,line) => {
            return sum + (line.product_id?.volume || 0) * line.getQuantity()
        },0);

        order.nf_order_total_weight = totalWeight;
        order.nf_order_total_volume = totalVolume;
        
        for (let line of lines){                        
            line.nf_volume = line.product_id.volume;
            line.nf_weight = line.product_id.weight;
            line.nf_total_volume = (line.product_id?.volume || 0) * line.getQuantity();
            line.nf_total_weight = (line.product_id?.weight || 0) * line.getQuantity();
        }

        await super.validateOrder(...arguments);
    }
})