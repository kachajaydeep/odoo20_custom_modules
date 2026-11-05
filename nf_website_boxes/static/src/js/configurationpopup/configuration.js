import { _t } from '@web/core/l10n/translation';
import { patch } from '@web/core/utils/patch';
import { useSubEnv, useState } from '@odoo/owl';
import { ProductConfiguratorDialog } from '@sale/js/product_configurator_dialog/product_configurator_dialog';
import { QuantityButtons } from '@sale/js/quantity_buttons/quantity_buttons';
import { Product } from '@sale/js/product/product';
import { ComboConfiguratorDialog } from '@sale/js/combo_configurator_dialog/combo_configurator_dialog';

var self = ""

patch(Product, {
    props: {
        ...Product.props, 
        nf_box_item_count: { type: Number, optional: true }
    },
});
patch(QuantityButtons, {
    props: {
        ...QuantityButtons.props,
        nf_is_disabled:  { type: Boolean, optional: true },
    }
})
patch(ProductConfiguratorDialog.prototype, {
    setup() {
        super.setup(...arguments)
        self = this;
        this.max_box_count = this.state.products[0]?.nf_box_item_count || 0;
        self.max_box_count = this.state.products[0]?.nf_box_item_count || 0;

        useSubEnv({
            nf_optional_product_limit: this.nf_optional_product_limit // (self)
        })
    },
    async _setQuantity(productTmplId, quantity) {
        await super._setQuantity(...arguments);
        this.render(true);  
    },


    async _addProduct(productTmplId) {
        await super._addProduct(...arguments)
        this.render(true)
    },
    nf_optional_product_limit(){    
        let total_product_qty = self.state?.products.map((x) => x.nf_box_item_count <= 0 ?  x.quantity : 0);
    
        if (total_product_qty.length){
            let main_pro_qty = self.state?.products[0].quantity
            let totalQty = total_product_qty?.reduce((a,b) => a + b);
            if (totalQty >= (self.max_box_count * main_pro_qty)){
                return true
            }else{
                return false
            }
        }else{
            return false
        }
        
    }
})