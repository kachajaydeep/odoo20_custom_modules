import {
    PosOrderline
} from "@point_of_sale/app/models/pos_order_line";
import {
    patch
} from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    setup(vals) {
        this.nf_section = this.nf_section || "";
        return super.setup(...arguments);
    },
    getDisplayData() {
        var creationOrderLine = super.getDisplayData();

        if (this.nf_section) {
            creationOrderLine["nf_section"] = this.nf_section;
        }

        return creationOrderLine;
    },
    can_be_merged_with(orderline) {
        let res = super.can_be_merged_with(...arguments)
        if (this.nf_section) {
            return false
        } else {
            return res
        }
    }
})