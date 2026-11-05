
/** @odoo-module */

import { Order, Orderline, Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        if ( this.pos.config.nf_restrict_return_order ){
            this.allow_to_refund = json.return_exprired
        }else{
            this.allow_to_refund = false
        }
    },

})