import { Component, props, t } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class NfPrintPopup extends Component{
    static template = "nf_pos_receipt_a4_size.NfPrintPopup";
    static components = { Dialog }
}