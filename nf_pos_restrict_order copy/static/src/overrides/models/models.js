
/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";

patch(PosOrderline.prototype, {
    getDisplayData() {
        var res = super.getDisplayData(...arguments)
        
        return res
    },
    getDisplayClasses() {
        var res = super.getDisplayClasses();
        var product = this.getProduct()
        let stocks = this.models['stock.quant'].filter((x) => (x.product_id?.id == product.id) && x.location_id.id == posmodel.pickingType.default_location_src_id.id );
        let list_stock = stocks.map((x) => x.quantity)
        let quantity = 0.00
        if (list_stock.length){
            quantity = list_stock.reduce((prev, current) => prev + current);
        }      
        var remain = quantity - this.qty
        res['nf_positive_line'] = remain > 0  ? true : false
        res['nf_nagitive_line'] = remain <= 0 ? true : false        
        return res
    },
})

patch(PosOrder.prototype, {
     
})