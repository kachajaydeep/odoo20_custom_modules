/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {
    async addLineToCurrentOrder(vals, opts = {}, configure = true) {  
        let order = this.getOrder();
        
        return await this.addLineToOrder(vals, order, opts, configure);
    }
})