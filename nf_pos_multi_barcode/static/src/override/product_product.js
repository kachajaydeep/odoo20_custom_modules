/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ProductProduct } from "@point_of_sale/app/models/product_product"

patch(ProductProduct.prototype, {
    get searchString() {
        const result = super.searchString;
        if (!posmodel?.config.nf_enable_pos_multi_barcode) { return result; }

        const extraBarcodes = (this.barcode_ids || [])
            .map(barcode => barcode.name)
            .filter(Boolean)
            .join(" ");
        return `${result} ${extraBarcodes}`.trim();
    }
});