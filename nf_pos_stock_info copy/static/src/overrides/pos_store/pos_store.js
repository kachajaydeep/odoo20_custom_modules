import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {
    async validateOrder(args = {}) {
        if (this.config.nf_pos_enable_stock_info) {
            const order = this.getOrder();
            const lines = order.getOrderlines();
            const quants = this.models["stock.quant"] || [];

            for (const line of lines) {
                const product = line.getProduct();
                const stock = quants.filter((quant) => {
                    return (
                        quant.product_id?.id === product.id &&
                        quant.location_id?.id ===
                        this.pickingType.default_location_src_id.id
                    );
                });

                if (stock.length > 0) {
                    stock[0].quantity =
                        (stock[0].quantity || 0) - line.qty;
                    stock[0].available_quantity =
                        (stock[0].available_quantity || 0) - line.qty;
                }
                else {
                    this.models["stock.quant"].create({
                        product_id: product,
                        location_id: this.pickingType.default_location_src_id,
                        quantity: -line.qty,
                        available_quantity: -line.qty,
                    });
                }
            }
        }
        await super.validateOrder(...arguments);
    }
})