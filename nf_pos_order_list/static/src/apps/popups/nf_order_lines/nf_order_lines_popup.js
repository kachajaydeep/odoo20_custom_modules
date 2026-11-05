import { Component  } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class nfPosOrderLinesPopup extends Component {
    static template = "nf_pos_order_list.nfPosOrderLinesPopup";
    static components = { Dialog };
}
