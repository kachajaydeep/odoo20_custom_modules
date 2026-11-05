/** @odoo-module **/

import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    setup() {
        super.setup(...arguments);
    },
    // getDisplayData() {
    //     var result = super.getDisplayData()
    //     result['nf_get_disount_price'] =  this.nf_get_disount_price()  || false
    //     result['finalized'] =  this.order_id.finalized || false
    //     return result
    // },
});
