import { Component, onWillStart, onMounted, proxy } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class NfSelectLotPopup extends Component {
    static template = "nf_pos_product_lot_selection.NfSelectLotPopup";
    static components = { Dialog, };
    static props = {
        array: Array,
        title: String,
        name: String,
        isSingleItem: Boolean,
        close: Function,
        getPayload: Function,
        productId: Number,
        options: { type: Array, optional: true },
        uniqueValues: { type: Boolean, optional: true },
        selectedLot: { type: String, optional: true },
        lotQty: { type: Number, optional: true },
    };

    setup() {
        this.lots = proxy([]);
        this.lot_detail = proxy([]);

        if (this.props.selectedLot && this.props.lotQty) {
            this.lot_detail.push({
                lot_name: this.props.selectedLot,
                qty: Number(this.props.lotQty),
            });
        }

        onMounted(() => {
            if (!this.env.services.pos.config.nf_enable_lot_selection) { return; }

            if (!this.props.selectedLot) { return; }

            const input = document.querySelector(
                `input[lot_name="${CSS.escape(this.props.selectedLot)}"]`
            );

            if (input) {
                input.value = this.props.lotQty;
            }
        });

        onWillStart(async () => {
            await this.loadProductLots();
        });
    };

    async loadProductLots() {
        const productId = this.props.productId;

        if (!productId) {
            this.lots.splice(0, this.lots.length);
            return;
        }

        const lots = await this.env.services.orm.call(
            "stock.lot",
            "get_pos_lots",
            [productId]
        );

        this.lots.splice(0,
            this.lots.length,
            ...(lots || [])
        );
    }

    getLotQty(lotName) {
        const lot = this.lot_detail.find(
            (item) => item.lot_name === lotName
        );

        return lot ? lot.qty : "";
    }

    updateLotQty(event) {
        const input = event.target;
        const lotName = input.getAttribute("lot_name");
        const rawValue = input.value.trim();
        const qty = parseFloat(rawValue);

        if (!lotName) {
            return;
        }

        const existingIndex = this.lot_detail.findIndex(
            (lot) => lot.lot_name === lotName
        );

        if (rawValue === "" || isNaN(qty) || qty <= 0) {
            if (existingIndex !== -1) {
                this.lot_detail.splice(existingIndex, 1);
            }
            return;
        }

        const lot = this.lots.find(
            (item) => item.name === lotName
        );

        let finalQty = qty;

        if (
            lot &&
            lot.product_qty !== undefined &&
            lot.product_qty !== null
        ) {
            finalQty = Math.min(qty, lot.product_qty);
        }

        const lotData = {
            lot_name: lotName,
            qty: finalQty,
        };

        if (existingIndex !== -1) {
            this.lot_detail.splice(existingIndex,
                1,
                lotData
            );
        } else {
            this.lot_detail.push(lotData);
        }

        input.value = finalQty;
    }

    confirm() {
        const payload = this.lot_detail.filter((lot) =>
            lot.lot_name &&
            lot.qty > 0
        );

        this.props.getPayload(payload);
        this.props.close();
    }
    
    close() {
        this.props.close();
    };
}