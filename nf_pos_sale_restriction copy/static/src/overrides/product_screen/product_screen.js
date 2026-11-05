import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";
import { ask } from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(ProductScreen.prototype, { 
    
    async addProductToOrder(product) {
        const result = await super.addProductToOrder(product);

        if (!this.pos.config.nf_pos_enable_stock_restriction) { return result; }

        const order = this.pos.getOrder();
        const line = order.getSelectedOrderline();

        if (!line) { return; }

        const lineProduct = line?.getProduct();
        const comboLines = line?.combo_line_ids || [];

        if (lineProduct?.type == 'combo'){
            for (let combo_line of comboLines){
                const comboProduct = combo_line.getProduct?.() || combo_line.product_id;
                
                const combo_product_stock = await this.pos.models['stock.quant'].find(
                    (x) =>
                        x.product_id?.id === comboProduct?.id &&
                        x.location_id.id === this.pos.pickingType.default_location_src_id.id
                );

                const line_qty = comboProduct?.qty_available;
                const combo_stock_qty = combo_product_stock?.available_quantity || 0;
                const qty_available = Math.max(line_qty, combo_stock_qty);
                const current_qty = combo_line.qty;

                if (qty_available >= (current_qty + 1)) {
                    continue;
                }
    
                if (this.pos.config.nf_to_sale_more_than_on_hand) {
                    const response = await ask(this.dialog, {
                        title: _t("Product Stock"),
                        body: _t(
                            "You do not have enough stock of Product " + combo_line.full_product_name + "!"
                        ),
                        confirmLabel: _t("Order"),
                        cancelLabel: _t("Cancel"),
                    });
                    console.log("Response", response);

                    if (!response) {
                        if (current_qty > 1) {
                            combo_line.set_quantity(current_qty - 1);
                        } else {
                            order.removeOrderline(line);
                        }
                    }
                } else {
                    if (current_qty > 1) {
                        combo_line.set_quantity(current_qty - 1);
                    } else {
                        order.removeOrderline(line);
                    }
    
                    this.dialog.add(AlertDialog, {
                        title: _t("Product Stock"),
                        body: _t(
                            "You do not have enough stock of Product " +
                            lineProduct.display_name +
                            "!"
                        ),
                    });
                    return result;
                }
            }
        }
        else {
            const stock = this.pos.models['stock.quant'].find(
                (x) => 
                    x.product_id?.id === lineProduct.id &&
                    x.location_id.id === this.pos.pickingType.default_location_src_id.id
            );

            const qty_available = stock?.available_quantity ?? lineProduct?.qty_available ?? 0;
            const current_qty = line.qty;            
            
            if (qty_available >= (current_qty + 1)){ return result; }

            else{
                if (this.pos.config.nf_to_sale_more_than_on_hand){
                    const response = await ask(this.dialog, {
                        title: _t(" Product Stock "),
                        body: _t("You do not have enough stock of Product " + product.display_name + " !"),
                        confirmLabel: _t("Order"),
                        cancelLabel: _t("Cancel"),
                    });
                    if (response) {
                        return result;
                    }

                    order.removeOrderline(line);
                }else{
                    this.dialog.add(AlertDialog,{
                        title: _t("Product Stock"),
                        body: _t("You do not have enough stock of Product " + product.display_name + " !"),
                    });
                    order.removeOrderline(line);
                }
            }
            return result;
        }
    }
});

patch(OrderSummary.prototype,{
    async updateSelectedOrderline({ buffer, key }) {
        
        if (!this.pos.config.nf_pos_enable_stock_restriction || this.pos.numpadMode !== "quantity"){
            return await super.updateSelectedOrderline(...arguments);
        }

        // Let Odoo handle editing keys such as Backspace.
        if (key === "Backspace" || key === "Delete") {
            return await super.updateSelectedOrderline(...arguments);
        }

        const qty = parseFloat(buffer);
        const selectedLine = this.currentOrder.getSelectedOrderline();

        if (!selectedLine) { return; }

        const product = selectedLine.getProduct();
        const stock = this.pos.models['stock.quant'].find(
            (x) => 
                x.product_id?.id == product.id && 
                x.location_id.id == this.pos.pickingType.default_location_src_id.id
        );

        const qty_available = stock?.available_quantity ?? product.qty_available ?? 0;
        
        if (qty_available >= qty) { return await super.updateSelectedOrderline(...arguments); }

        if (this.pos.config.nf_to_sale_more_than_on_hand){
            const response = await ask(this.dialog, {
                title: _t(" Product Stock "),
                body: _t("You do not have enough stock of Product " + product.display_name + " !"),
                confirmLabel: _t("Order"),
                cancelLabel: _t("Cancel"),
            });
            if (response) {
                await super.updateSelectedOrderline(...arguments);
            }

            this.numberBuffer.reset();
        }

        this.dialog.add(AlertDialog,{
            title: _t("Product Stock"),
            body: _t("You do not have enough stock of Product " + product.display_name + " !"),
        });

        this.numberBuffer.reset();
    }
});