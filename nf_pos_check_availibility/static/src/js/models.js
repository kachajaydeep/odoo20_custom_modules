/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";

patch(PosOrderline.prototype, {
    setup(vals) {
        super.setup(...arguments);
        this.nf_stock_availability = undefined;
    },

    getDisplayClasses() {
        const res = super.getDisplayClasses();
        if (this.nf_stock_availability === true) {
            res['nf-is-available'] = true;
        } else if (this.nf_stock_availability === false) {
            res['nf-is-not-available'] = true;
        }
        return res;
    },
});