/** @odoo-module */

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";
import { ask } from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(ProductScreen.prototype, { 
    
    async addProductToOrder(product) {
        debugger
        let stock = this.pos.models['stock.quant'].filter((x) => (x.product_id?.id == product.product_variant_id.id) && x.location_id.id == this.pos.pickingType.default_location_src_id.id );
        let qty_available = 0
        if (stock && stock[0]){
            qty_available = stock[0].available_quantity
        }else{
            qty_available = product.qty_available
        }
        
        let selected_line = this.pos.getOrder().getOrderlines().filter((line) => line.product_id.id == product.product_variant_id.id)
        var currunt_qty = selected_line.length ? selected_line[0].qty : 0 
        if (this.pos.config.nf_pos_enable_stock_info){
            if (qty_available >= (currunt_qty + 1)){
                await super.addProductToOrder(...arguments)
            }else{
                if (this.pos.config._nf_to_sale_morthan_on_hand){
                    const response = await ask(this.dialog, {
                        title: _t(" Product Stock "),
                        body: _t("You do not have enough stock of Product " + product.display_name + " !"),
                        confirmLabel: _t("Order"),
                        cancelLabel: _t("Cancel"),
                    });
                    if (response) {
                        await super.addProductToOrder(...arguments)
                    }
                }else{
                    this.dialog.add(AlertDialog,{
                        title: _t("Product Stock"),
                        body: _t("You do not have enough stock of Product " + product.display_name + " !"),
                    });
                }
            }
        }else{
            await super.addProductToOrder(...arguments)
        }
    }
});

patch(OrderSummary.prototype,{
    async updateSelectedOrderline({ buffer, key }) {
        
        if (this.pos.config.nf_pos_enable_stock_info && this.pos.config._nf_pos_enable_stock_restriction &&  this.pos.numpadMode == "quantity" ){
            let qty = parseFloat(buffer) 
            let selectedLine = this.currentOrder.getSelectedOrderline();
            let product = selectedLine.getProduct()
             let stock = this.pos.models['stock.quant'].filter((x) => (x.product_id?.id == product.id) && x.location_id.id == this.pos.pickingType.default_location_src_id.id );
            let qty_available = 0
             if (stock && stock[0]){
                qty_available = stock[0].available_quantity
            }else{
                qty_available = product.qty_available
            }
            if (qty_available < qty){
                if (this.pos.config._nf_to_sale_morthan_on_hand){
                    const response = await ask(this.dialog, {
                        title: _t(" Product Stock "),
                        body: _t("You do not have enough stock of Product " + product.display_name + " !"),
                        confirmLabel: _t("Order"),
                        cancelLabel: _t("Cancel"),
                    });
                    if (response) {
                        await super.updateSelectedOrderline(...arguments)
                    }else{
                        this.numberBuffer.reset();
                    }
                }else{
                    this.dialog.add(AlertDialog,{
                        title: _t("Product Stock"),
                        body: _t("You do not have enough stock of Product " + product.display_name + " !"),
                    });
                    this.numberBuffer.reset();
                }
            }else{
                await super.updateSelectedOrderline(...arguments)
            }
        }else{
            await super.updateSelectedOrderline(...arguments)
        }
    },
})