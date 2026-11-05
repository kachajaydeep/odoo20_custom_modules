import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(Orderline.prototype, {
    get lineScreenValues() {
        const values = super.lineScreenValues;

        if(this.env.services.pos.config.allow_secondary_uom){
            const line = this.line;
    
            // Only intervene when a custom UOM was selected
            if (!line.selected_uom_id) {
                return values;
            }
    
            const basic = this.props.basic_receipt;
            const mode = this.props.mode;
    
            // Force show the unit price line even when qty === 1
            const showPrice =
                !basic &&
                (mode === "receipt" || (line.price_type !== "original" && !line.combo_parent_id));
    
            const priceUnit = `${line.currencyDisplayPriceUnit} / ${line.selected_uom_id.name}`;
    
            return {
                ...values,
                displayPriceUnit: showPrice && line.price !== 0 && priceUnit,
            };
        }
        return values;
    }
});

patch(PosStore.prototype, {
    async addLineToCurrentOrder(vals, opts = {}, configure = true) {
        const result = await super.addLineToCurrentOrder(vals, opts, configure);

        const line = this.getOrder()?.getSelectedOrderline();
        if (!line) return result;
        
        const product = line.product_id;
        
        line.selected_uom_id = product.uom_id || null;

        if (!this.config.allow_secondary_uom) return result;

        if (product.is_default_uom && product.default_uom_id) {
            try{
                const updated_price = await this.getUpdatedPrice(
                    product.product_tmpl_id.id,
                    product.default_uom_id.id
                );
    
                if (updated_price !== null) {
                    line.selected_uom_id = product.default_uom_id;
                    line.setUnitPrice(updated_price);
                    line.price_type = "manual";
                }
            } catch(e) {
                console.error("Failed to apply default UOM price", e);
            }
        }
        return result;
    },
    async getUpdatedPrice(product_tmpl_id, uom_id) {
        const orm = this.env.services.orm;

        return await orm.call(
            "product.template",
            "get_price_for_uom",
            [product_tmpl_id, uom_id],
        );
    }
});