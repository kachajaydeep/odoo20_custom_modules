import { Component, proxy } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { useService, useBus } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

export class NfStockMovePopup extends Component {
    static template = "nf_pos_stock_request.NfStockMovePopup";
    static components = { Dialog };

    static props = {
        title:{type:String,optional:true},
        moves:{type:Array,optional:true},
        showApprove:{type:Boolean,optional:true},
        incoming:{type:Array,optional:true},
        onApprove:{type:Function,optional:true}
    }

    setup() {
        this.orm = useService("orm");
        this.pos = usePos();
        this.notification = useService("notification");
        this.state = proxy({
            moves: this.props.moves.map(move => ({
                ...move,
                quantity: move.quantity || move.product_uom_qty 
            })),
        });
    }
    async approvePicking() {
        try {
            const pickingId = this.props.moves[0].picking_id.id;
            const moveData = this.state.moves.map(move => ({
                id: move.id,
                quantity: move.quantity || 0
            }));

            const result = await this.orm.call(
                "stock.picking",
                "action_validate_from_pos",
                [pickingId, moveData]
            );

            if (result) {
                if (this.props.onApprove) {
                    this.props.onApprove();
                }
                
                this.notification.add(_t("Transfer approved successfully."), { type: "success" });
                this.props.close({ confirmed: true });
            } else {
                this.notification.add(_t("Failed to approve transfer."), { type: "danger" });
            }
        } catch (error) {
            console.error("Error approving transfer:", error);
            this.notification.add(_t("An error occurred while approving."), { type: "danger" });
        }
    }

    closePopup() {
        this.props.close();
    }
}
