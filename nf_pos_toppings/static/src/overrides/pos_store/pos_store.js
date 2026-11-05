import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";
import { ToppingsPopup } from "@nf_pos_toppings/apps/toppings_popup/toppings_popup"
import {
    makeAwaitable,
    ask,
    makeActionAwaitable,
} from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(PosStore.prototype, {

  async addLineToOrder(vals, order, opts = {}, configure = true) {
    let parentLine = await super.addLineToOrder(...arguments);
    const product = vals.product_tmpl_id;
    
    // let selectedline = this.getOrder().getSelectedOrderline();

    if(product.topping_group_ids.length > 0){
        let $productPayload = await makeAwaitable(
            this.dialog,
            ToppingsPopup,
            {
                product_toppings:product.topping_group_ids,
                product_obj:product,
            }
        )
                
        if (!$productPayload || !$productPayload.length) {
            return parentLine;
        }
        for(let product of $productPayload){
            const price = product.lst_price;
            parentLine.price_unit += price
            if(product){
                let childline = await this.addLineToCurrentOrder({
                    product_id:product,
                    product_tmpl_id:product.product_tmpl_id,
                    price_unit:0,
                    qty:1,
                    nf_child_orderline_id: parentLine,
                },{ merge:false });
            }
        }
        // parentLine.price_unit = this.get_order().get_total_with_tax();
    }
    
  },
});
