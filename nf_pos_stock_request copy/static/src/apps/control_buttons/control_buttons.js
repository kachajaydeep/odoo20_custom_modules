import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import {
    makeAwaitable,
    ask,
    makeActionAwaitable,
} from "@point_of_sale/app/utils/make_awaitable_dialog";
import { useService } from "@web/core/utils/hooks";
import { NfStockRequestPopup } from "@nf_pos_stock_request/apps/popup/stock_request_popup/stock_request_popup";
import { NfStockHistoryPopup } from "@nf_pos_stock_request/apps/popup/stock_history_popup/stock_history_popup";
import { NfStockPickingHistory } from "@nf_pos_stock_request/apps/screens/nf_stock_picking_history";
import { proxy } from "@odoo/owl";

patch(ControlButtons.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        this.state = proxy({
            pickings:[],
            quants:[],
        })
    },

    async requestProductQuotation() {
        if(this.pos.config.nf_enable_stock_request){           
            const orderline = this.pos.getOrder().getSelectedOrderline();
            if (!orderline) return;
            
            const product = orderline.product_id;
            const self_location_id = this.pos.config.picking_type_id.default_location_src_id.id;
            this.state.quants = [];

            const stock_quants = await this.pos.data.call(
                "stock.quant",
                "search_read",
                [
                    [
                        ["product_id", "=", product.id],
                        ["location_id", "!=", self_location_id],
                        ["quantity", ">", 0],
                    ]
                ],

            );

            for(let quant of stock_quants){
                if(!this.state.quants.includes(quant)){
                    this.state.quants.push(quant)
                }
            }
        
            if(this.state.quants.length){
                const $nfstockpayload = await makeAwaitable(
                    this.dialog,
                    NfStockRequestPopup,
                    {
                        quants: this.state.quants,
                        title: _t("Request Stock for %s", product.display_name),
                        cancelText: _t("Cancel"),
                        confirmText: _t("Confirm"),
                    }
                );
            }
            else{
                this.notification.add(_t("The selected product has no available stock in internal transfers."), { type: "warning" });
            }
        }
        
    },

    async requestHistoryQuotation() {   
        const my_location_id = this.pos.config.picking_type_id.default_location_src_id.id;
        
        const nfstockpickings = await this.pos.data.searchRead(
            "stock.picking",
                   [
            "|",
            ["location_id", "=", my_location_id],
            ["location_dest_id", "=", my_location_id],
        ]
        );
        for (const picking of nfstockpickings) {
            if (picking.move_ids.length > 0) {
                const moves = await this.pos.data.read("stock.move", [picking.move_ids[0]], ["description_picking", "picking_id"]);
                if (moves.length > 0) {my_location_id
                    this.state.pickings.push({
                        id: picking.id,
                        product_name: moves[0].description_picking,
                        picking_id: moves[0].picking_id,
                        location_id: picking.location_id,
                        location_dest_id: picking.location_dest_id,
                        state: picking.state,
                        type: picking.location_dest_id[0] === my_location_id ? "Incoming" : "Outgoing"
                    });
                }
            }
        }
        if(this.pos.config.nf_enable_stock_request){
            this.pos.navigate("NfStockPickingHistory", {
                pickings: this.state.pickings
            });
        }
    }
});