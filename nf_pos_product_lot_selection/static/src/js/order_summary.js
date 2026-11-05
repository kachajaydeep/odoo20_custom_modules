import "@pos_stock/app/screens/product_screen/order_summary/order_summary";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { NfSelectLotPopup } from "@nf_pos_product_lot_selection/popups/nf_select_lot_popup";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";

patch(OrderSummary.prototype, {
    async editPackLotLines(line) {
        if (!this.pos.config.nf_enable_lot_selection) {
            return await super.editPackLotLines(line);
        }

        const product = line.product_id;
        const isSingleItem = line.product_id.tracking === "serial";

        const lots = await this.env.services.orm.call(
            "stock.lot",
            "get_pos_lots",
            [product.id]
        );
        
        const existingLots = line.pack_lot_ids.map(lot => ({
            id: lot.id,
            text: lot.lot_name,
            qty: line.qty,
        }));

        const payload = await makeAwaitable(this.dialog, NfSelectLotPopup,
            {
                title: _t("Lot/Serial Number(s) Required"),
                name: product.display_name,
                isSingleItem,
                array: existingLots,
                options: lots.map(lot => lot.name),
                uniqueValues: isSingleItem,
                productId: product.id,
                selectedLot: line.pack_lot_ids[0]?.lot_name || "",
                lotQty: line.qty,
            }
        );

        if (!payload) { return; }

        const newLotLines = payload
            .filter((item) => item.lot_name && item.qty > 0)
            .map((item) => ({
                lot_name: item.lot_name,
            }));

        let modifiedPackLotLines = {};

        if (line.pack_lot_ids.length && newLotLines.length) {
            modifiedPackLotLines = {
                [line.pack_lot_ids[0].id]: newLotLines[0].lot_name,
            };
        }

        line.setPackLotLines({
            modifiedPackLotLines,
            newPackLotLines: line.pack_lot_ids.length
                ? []
                : newLotLines,
            setQuantity: false,
        });

        const quantity = payload.reduce(
            (total, item) => total + (parseFloat(item.qty) || 0),
            0
        );

        if (quantity > 0) {
            line.setQuantity(quantity);
        }

        this.pos.getOrder()?.selectOrderline(line);
    },
})
