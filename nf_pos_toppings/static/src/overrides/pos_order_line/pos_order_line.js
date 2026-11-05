import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    setup(vals) {
        super.setup(...arguments);
        this.nf_child_orderline_id = vals?.nf_child_orderline_id || null;
    },
    // getDisplayData(){
    //     let creationOrderLine = super.getDisplayData();

    //     if(this.nf_child_orderline_id){
    //         creationOrderLine["nf_child_orderline_id"] = this.nf_child_orderline_id;
    //     }
    //     return creationOrderLine;
    // },
    export_as_JSON(){
        const json = super.export_as_JSON(...arguments);
        json.nf_child_orderline_id = this.nf_child_orderline_id || "";
        return json;
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.nf_child_orderline_id = json.nf_child_orderline_id || "";
    }
})