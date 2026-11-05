import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype,{
    get productsToDisplay() {
        let result = super.productsToDisplay;
        const value = this.nfProductToSearchVendor;
    
        if (!value) {
            return result;
        }

        else if(value && this.config.nf_product_search_by_vendor) {
            let products = [];
            let vendors = this.models["product.supplierinfo"].getAll();
            
            let searched_vendors = vendors.filter((vendor) => {
                return vendor.display_name
                    .trim()
                    .toLowerCase()
                    .includes(value.trim().toLowerCase());
            });
            for (let index = 0; index < searched_vendors.length; index++) {
                const vendor = searched_vendors[index];
                
                let temp = result.filter(
                    (product) =>
                        product.id == vendor.product_tmpl_id?.id
                );
                
                temp.forEach((product) => {
                    if (!products.find(p => p.id === product.id)) {
                        products.push(product);
                    }
                });
            }

            return products;
        }        
    },
})