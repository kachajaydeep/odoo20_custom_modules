/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";


patch(PosStore.prototype, {
    get_order_section_demo_product () {
        return Object.values(this.db.product_by_id).filter((x) => x.nf_demo_product_for_sale_section)[0]
    }
})