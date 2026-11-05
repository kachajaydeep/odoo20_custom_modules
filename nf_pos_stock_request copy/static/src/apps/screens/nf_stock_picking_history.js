import { Component, onWillStart, proxy } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useService, useBus } from "@web/core/utils/hooks";
import { NfStockMovePopup } from "@nf_pos_stock_request/apps/popup/stock_move_popup/stock_move_popup";
import {
    makeAwaitable,
    ask,
    makeActionAwaitable,
} from "@point_of_sale/app/utils/make_awaitable_dialog";

export class NfStockPickingHistory extends Component {
    static template = "nf_pos_stock_request.NfStockPickingHistory";
    setup() {
        this.pos = usePos();
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.state = proxy({
            incoming: [],
            outgoing: [],
            loading: false,
            activeTab: 'incoming',
        });
        this.dialog = useService("dialog");

        useBus(this.pos.bus, "new-stock-request", (payload) => this.onNewStockRequest(payload));
        useBus(this.pos.bus, "REMOVE_STOCK_RECORD", (ev) => {
            const { pickingId } = ev.detail;
            this.state.incoming = this.state.incoming.filter(p => p.id !== pickingId);
            const outgoing = this.state.outgoing.find(p => p.id === pickingId);
            if (outgoing) {
                outgoing.state = "done";
            }
        });

        onWillStart(async () => {
            await this.fetchPickings();
        });
    }

    onNewStockRequest(newpayload) {
        let payload = newpayload.detail;
        const my_location_id = this.pos.config.picking_type_id.default_location_src_id.id;
        
        if (this.state.incoming.find(p => p.id === payload.id) || this.state.outgoing.find(p => p.id === payload.id)) {
            return;
        }

        const picking_data = {
            id: payload.id,
            move_id: payload.move_id,
            product_name: payload.product_name,
            picking_id: payload.picking_id,
            location_id: payload.location_id,
            location_dest_id: payload.location_dest_id,
            state: payload.state,
        };

        if (payload.location_id[0] === my_location_id) {
            this.state.incoming = [picking_data, ...this.state.incoming];
        } else {
            this.state.outgoing = [picking_data, ...this.state.outgoing];
        }
    }

    async fetchPickings() {
        this.state.loading = true;
        try {
            const my_location_id = this.pos.config.picking_type_id.default_location_src_id.id;
            const domain = [
                "&",
                ["picking_type_id.code", "=", "internal"],
                "|",
                ["location_id", "=", my_location_id],
                ["location_dest_id", "=", my_location_id]
            ];
            
            const nf_pickings = await this.orm.searchRead(
                "stock.picking",
                domain,
                ["id", "move_ids", "location_id", "location_dest_id", "state", "name"]
            );
            
            const incoming = [];
            const outgoing = [];

            for (const picking of nf_pickings) {
                if (picking.move_ids.length > 0) {
                    const moves = await this.orm.read("stock.move", [picking.move_ids[0]], ["description_picking", "picking_id", "product_id"]);
                    if (moves.length > 0) {
                        const picking_data = {
                            id: picking.id,
                            move_id: moves[0].id,
                            product_name: moves[0].description_picking,
                            picking_id: moves[0].picking_id,
                            location_id: picking.location_id,
                            location_dest_id: picking.location_dest_id,
                            state: picking.state,
                            date: picking.date,
                        };
                        
                        if (picking.location_id[0] === my_location_id) {
                            incoming.push(picking_data);
                        } else {
                            outgoing.push(picking_data);
                        }
                    }
                }
            }
            
            this.state.incoming = incoming;
            this.state.outgoing = outgoing;
        } catch (error) {
            this.notification.add("Failed to refresh transfers.", { type: "danger" });
        } finally {
            this.state.loading = false;
        }
    }

    switchTab(tab) {
        this.state.activeTab = tab;
    }

    async acceptPicking(picking) {
       this.state.loading = true;
        try {
            const moves = await this.pos.data.searchRead(
                "stock.move",
                [["picking_id", "=", picking.id]],
                ["product_id", "product_uom_qty", "quantity", "state"]
            );

            const quants = await this.pos.data.searchRead(
                "stock.quant",
                [
                    ["product_id", "in", moves.map(m => Array.isArray(m.product_id) ? m.product_id[0] : m.product_id)],
                    ["location_id", "=", picking.location_id[0]]
                ],
                ["product_id", "quantity"]
            );

            const quantMap = quants.reduce((acc, q) => {
                const prodId = Array.isArray(q.product_id) ? q.product_id[0] : q.product_id;
                acc[prodId] = (acc[prodId] || 0) + q.quantity;
                return acc;
            }, {});

            const enrichedMoves = moves.map(move => {
                const prodId = Array.isArray(move.product_id) ? move.product_id[0] : move.product_id;
                const product = this.pos.models['product.product'].find(p => p.id === prodId);
                return {
                    ...move,
                    product_name: product ? product.display_name : (Array.isArray(move.product_id) ? move.product_id[1] : `Product #${move.product_id}`),
                    availability: quantMap[prodId] || 0
                };
            });
            
            for(let move of moves){
                const enriched = enrichedMoves.find(m => m.id === move.id);
                move.picking_id = picking;
                move.product_name = enriched.product_name;
                move.availability = enriched.availability;
            }

            const result = await makeAwaitable(
                this.dialog,
                NfStockMovePopup,
                {
                    title: `Lines for ${picking.picking_id[1]}`,
                    moves: moves,
                    // showApprove: this.state.activeTab === 'incoming' && picking.state !== 'done',
                    showApprove: this.state.activeTab === 'incoming' && picking.state !== 'done' && this.pos.config.nf_is_inventory_admin,
                    incoming:this.state.incoming.filter(p => p.id !== picking.id),
                    onApprove: () => {
                        const incoming = this.state.incoming.find(p => p.id === picking.id);
                        if (incoming) {
                            incoming.state = "done";
                        }
                        const outgoing = this.state.outgoing.find(p => p.id === picking.id);
                        if (outgoing) {
                            outgoing.state = "done";
                        }
                    
                    }
            });
            if (result && result.confirmed) {
                await this.fetchPickings();
            }

        } catch (error) {
            console.error("Error fetching stock moves:", error);
            this.notification.add("Could not fetch move details.", { type: "danger" });
        } finally {
            this.state.loading = false;
        }
    }

    closeCustomScreen() {
        const order = this.pos.getOrder();

        if (order) {
            this.pos.navigate("ProductScreen", { orderUuid: order.uuid });
        } else {
            this.pos.navigate("ProductScreen");
        }
    }
}

registry.category("pos_pages").add("NfStockPickingHistory", {
    name: "NfStockPickingHistory",
    component: NfStockPickingHistory,
    route: `/pos/ui/${odoo.pos_config_id}/pickinghistory`,
});