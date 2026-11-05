import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

patch(PosOrder.prototype, {
    set_pos_order(order_type){
        this.nf_pos_order_type_id = order_type;
        this.nf_name = order_type.name;
        return order_type
    },
    pos_order_type(){
      return this.nf_pos_order_type_id.name
    }
})