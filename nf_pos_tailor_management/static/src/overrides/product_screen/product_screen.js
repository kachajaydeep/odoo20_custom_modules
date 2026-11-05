import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { MrpBom } from "@nf_pos_tailor_management/app/bill_material/mrp_bom_popup"

patch(ProductScreen.prototype,{
    async addProductToOrder(product){
        let product_count = product.product_variant_ids[0].bom_count;
        let product_variant_bom_ids = product.product_variant_ids[0].bom_ids;
        let payload;

        if(product_count){
            payload = await makeAwaitable(
                this.dialog,
                MrpBom,
                {
                    bom_ids:product_variant_bom_ids, // model: mrp.bom
                    product:product.product_variant_ids[0], // product.product
                }
            );
        }
        
        if (product_count){
            if(!payload){
                return false;
            }
            else{
                await super.addProductToOrder(product);
                this.pos.getOrder().getSelectedOrderline().setMrpOrder(payload);
                return;
            }
        }
        await super.addProductToOrder(product);    
    }
})