import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { _t } from "@web/core/l10n/translation";
import { NfSelectLotPopup } from "@nf_pos_product_lot_selection/popups/nf_select_lot_popup";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(PosStore.prototype, {
    async addLineToOrder(vals, order, opts = {}, configure = true) {
        const productTemplate = vals.product_tmpl_id;
        const product = this.models["product.product"].find(
            (product) => product.product_tmpl_id?.id === productTemplate.id
        );

        if (configure &&
            this.config.nf_enable_lot_selection &&
            product?.isTracked()
        ) {
            
            const isAllowOnlyOneLot = product.isAllowOnlyOneLot();

            const lots = await this.env.services.orm.call(
                "stock.lot",
                "get_pos_lots",
                [product.id]
            );

            const payload = await makeAwaitable(this.dialog, NfSelectLotPopup, {
                title: _t("Lot/Serial Number(s) Required"),
                name: product.name,
                isSingleItem: isAllowOnlyOneLot,
                array: [],
                options: lots.map(lot => lot.name),
                uniqueValues: product.tracking === "serial",
                productId: product.id,
                selectedLot: "",
                lotQty: 0,
            });
            
            if (!payload?.length) { return; }

            let firstLine = null;

            for (const lot of payload) {
                if (!lot.lot_name || !lot.qty || lot.qty <= 0) { continue; }

                const lineVals = {
                    ...vals,
                    product_id: product,
                    qty: lot.qty,
                };

                const line = await super.addLineToOrder(
                    lineVals,
                    order,
                    { ...opts, code: undefined, },
                    false
                );

                if (!line) { continue; }

                line.setPackLotLines({
                    modifiedPackLotLines: {},
                    newPackLotLines: [ {
                        lot_name: lot.lot_name,
                    }, ],
                    setQuantity: false,
                });

                line.setQuantity(lot.qty);

                if (!firstLine) {
                    firstLine = line;
                }
            }

            if (firstLine) {
                this.selectOrderLine(order, firstLine);
            }

            this.numberBuffer.reset();
            return firstLine;
        }
        
        return await super.addLineToOrder(...arguments)
    },
})
