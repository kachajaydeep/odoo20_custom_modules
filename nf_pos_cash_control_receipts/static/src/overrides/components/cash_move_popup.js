import { patch } from "@web/core/utils/patch";
import { CashMovePopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_popup";

patch(CashMovePopup.prototype, {
    get currentOrder() {
        return this.pos.getOrder()
    },

    async confirm() {
        try {
            await super.confirm(...arguments);
            const order = this.currentOrder;

            if (this.pos.config.nf_enable_cash_in_ont_receipt && order) {
                const date = new Date();
                const formattedDate = [
                    date.getFullYear(),
                    String(date.getMonth() + 1).padStart(2, "0"),
                    String(date.getDate()).padStart(2, "0"),
                ].join("-");
                
                this.pos.navigate("CashinOutScreen", {
                    orderUuid: order.uuid,
                    amount: this.state.amount,
                    date: formattedDate,
                    type: this.state.type,
                    reason: this.state.reason,
                });
            }
        } catch (error) {
            console.error("Cash In/Out redirect error:", error);
        }
    },

    async CashInReceipt() {
        let self = this;
        let TotalCashData = await this.pos.data.call('account.bank.statement.line', 'search_read', [
            [
                ['pos_session_id', '=', self.pos.session.id]
            ]
        ], )
        
        if (TotalCashData && this.currentOrder) {
            this.pos.navigate("CashinOutScreen", {
                orderUuid: this.currentOrder.uuid,
                'TotalCashData': TotalCashData,
            });
        }
        this.props.close();
    }
})