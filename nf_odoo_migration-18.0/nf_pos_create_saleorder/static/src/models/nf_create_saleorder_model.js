/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { Order, Orderline, Payment } from "@point_of_sale/app/store/models";

patch(Orderline.prototype, { 
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.nf_section = json.nf_section || ""
    },
    set_orderline_section (value) {
        this.nf_section = value;
    },
    get_orderline_section () {
        return this.nf_section;
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.nf_section = this.nf_section;
        
        return json;
    },
    getDisplayData() {
        console.log('nf_section ---> ',this.nf_section);
        
        return {
            ...super.getDisplayData(),
            "nf_section": this.nf_section || "",
        };
    },
});