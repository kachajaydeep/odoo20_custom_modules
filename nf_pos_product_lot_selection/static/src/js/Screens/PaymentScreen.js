import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

patch(PaymentScreen.prototype, {
    async afterOrderValidation(...args) {
        const order = this.currentOrder;

        await super.afterOrderValidation(...args);

        for (const line of order.get_orderlines()) {
            if (!line?.product_id) { continue; }

            if (!["serial", "lot"].includes(line.product_id.tracking)) { continue; }

            if (!line.pack_lot_ids?.length) { continue; }

            const lotName = line.pack_lot_ids[0].lot_name;

            if (!lotName) { continue; }

            const lotsForProduct = this.pos.models["stock.lot"]?.filter(
                (lot) => lot.product_id?.id === line.product_id.id
            );

            if (!lotsForProduct?.length) { continue; }

            const matchedLot = lotsForProduct.find(
                (lot) => lot.name === lotName
            );

            if (matchedLot) {
                matchedLot.product_qty -= line.qty;
            }
        }
    },
});