import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

patch(PosOrder.prototype, {
    setup() {
        super.setup(...arguments);
        const config = this.config;
        
        if (config.nf_is_default_selection_customer &&
            config.nf_default_customer_id &&
            !this.getPartner()
        ) {
            const partnerId = config.nf_default_customer_id;

            if (partnerId) {
                this.setPartner(partnerId);
            }
        }
    },
})

