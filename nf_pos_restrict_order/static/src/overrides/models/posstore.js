/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { _t } from "@web/core/l10n/translation";

patch(PosStore.prototype, {
    async pay() {
        let line_filter = await this.getOrder().getOrderlines().filter((line) =>  {
            let product = line.getProduct()
            let stock = this.env.services.pos.models['stock.quant'].filter((x) => (x.product_id?.id == product.id) && x.location_id.id == posmodel.pickingType.default_location_src_id.id );
            
            if (stock && stock.length && (stock[0].quantity - line.qty) < 0){
                return true
            }else if (stock && stock.length == 0){
                return true
            }else{
                return false
            }
        } )
        
        console.log("payment make in custom",line_filter);

        if (line_filter && line_filter.length && this.config.nf_pos_restrict_out_of_stock && this.config.nf_pos_enable_stock_info  ){
            this.notification.add(_t("You don't have enough stock to process the order."), { type: "danger" }, 3000);
            return;
        }
        super.pay()
    }
})