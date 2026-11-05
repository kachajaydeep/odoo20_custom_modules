import { _t } from "@web/core/l10n/translation";
import {Component, onMounted, useRef} from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useService } from "@web/core/utils/hooks";

export class NfStockHistoryPopup extends Component {
    static template = "nf_pos_stock_request.NfStockHistoryPopup";
    static components = { Dialog };
}