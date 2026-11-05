import { patch } from "@web/core/utils/patch";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";

patch(PosOrderline.prototype, {
    setQuantity(quantity, keep_price) {
        const quant = typeof quantity === "number" ? quantity : parseFloat("" + (quantity ? quantity : 0));
        this.update_qty_after_remove(quant)
        var result = super.setQuantity(...arguments)
        return result
    },

    async update_qty_after_remove(quant){    
        var line = this   
        if (quant || quant==0){
            var dic = {
                location_id: posmodel.pickingType.default_location_src_id.id,
                product_id: line.product_id.id,
                minus_quantity: quant,
                config_id:posmodel.config.id,
                update_with_zero : true
            }
            
            await posmodel.data.call("pos.config", "send_notification", [[], dic ]);
            var element = document.querySelector('.nf_product_qty'+ this.product_id.id)
                    
            if(element){
                element.click()
            }
        }   
    }
})