import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype,{
    setup(vals) {
        this.nf_tailor_order_id = this.nf_tailor_order_id || false;
        super.setup(...arguments);
    },

    setMrpOrder(mrp_bom) {
        if (!mrp_bom) {
            return;
        }
        this.bom_id = mrp_bom.nf_bom_component_ids[0].bom_id;
        this.nf_bom_component_ids = mrp_bom.nf_bom_component_ids;
    },

    setDeliveryDate(deliverydate){
        this.nf_delivery_date = deliverydate;
    },

    setMeasurement(measurement){
        this.nf_measurement_id = measurement;
    },

    setTailorOrder(order){
        this.nf_tailor_order_id = order;
    }
})