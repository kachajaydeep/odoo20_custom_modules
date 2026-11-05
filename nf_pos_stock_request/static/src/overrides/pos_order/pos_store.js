/* global Sha1 */

import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";
import { CashierSelectionPopup } from "@pos_hr/app/components/popups/cashier_selection_popup/cashier_selection_popup";
import { makeAwaitable, ask } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { NumberPopup } from "@point_of_sale/app/components/popups/number_popup/number_popup";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

patch(PosStore.prototype, {
    async setup() {
        await super.setup(...arguments);
        if (this.config.nf_enable_stock_request) {
            this.data.connectWebSocket("ST_REQUEST_ARRIVE", (payload) => {
                this.env.services.notification.add(
                    `New Stock Request for ${payload.product_name} from ${payload.origin_pos}`,
                    {
                        type: "info",
                        sticky: true,
                        title: "Incoming Stock Request",
                    }
                );
    
                this.bus.trigger("new-stock-request", payload);
            });

            this.data.connectWebSocket("ST_REQUEST_APPROVED", (payload) => {
                if (payload.product_id && payload.quantity !== undefined) {
                    const quants = this.models['stock.quant'].filter(
                        (q) => (q.product_id?.id || q.product_id) === payload.product_id
                    );
                    if (quants.length > 0) {
                        if (payload.quantity !== undefined) {
                            quants[0].quantity = payload.quantity;
                        } else if (payload.change_qty !== undefined) {
                            quants[0].quantity = (quants[0].quantity || 0) + payload.change_qty;
                        }
                    }
                }

                if (payload.is_requester) {
                    this.env.services.notification.add(
                        `Your stock request for "${payload.product_name}" (${payload.picking_id[1]}) has been approved!`,
                        {
                            type: "success",
                            sticky: true,
                            title: "Stock Request Approved",
                        }
                    );
                }                
    
                this.bus.trigger('stock-updated', payload);
                this.bus.trigger("refresh-picking-history", payload);
            });

            this.data.connectWebSocket("APPROVE-RECORD-FROM-ANOTHER-USER",(payload) => {
                const pickingId = Array.isArray(payload.picking_id) 
                ? payload.picking_id[0] 
                : (payload.picking_id?.id || payload.picking_id);

                this.bus.trigger('REMOVE_STOCK_RECORD',{ pickingId });
                this.bus.trigger("refresh-picking-history", payload);
            })
        }
    },
});
