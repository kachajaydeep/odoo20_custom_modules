/** @odoo-module */

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component  } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";


export class nfPosOrderLinesPopup extends Component {
    static template = "nf_pos_order_list.nfPosOrderLinesPopup";
    static components = { Dialog };
    setup() {
        super.setup();
        this.pos = usePos();
    }
}
