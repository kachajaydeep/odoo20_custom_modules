import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { useBarcodeReader } from "@point_of_sale/app/hooks/barcode_reader_hook";
import { useService } from "@web/core/utils/hooks";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { ReturnOrderDialog } from "@nf_pos_barcode_return_exchange/apps/popups/return_order_popup";
import { _t } from "@web/core/l10n/translation";

patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.notification = useService("notification");
        useBarcodeReader({
            nf_order: (code) => this._barcodeReceiptAction(code),
        });
    },

    async _getOrderByBarcode(code) {
        const allOrders = this.pos.models["pos.order"].getAll();
        let order = allOrders.find((o) => o.nf_barcode_id === code);

        if (!order) {
            const result = await this.pos.data.searchRead(
                "pos.order",
                [["nf_barcode_id", "=", code]],
                [],
            );
            order = result.length ? result[0] : null;
        }
        
        return order || null;
    },

    async _getOrderLines(order){
        const orderlines = this.pos.data.searchRead(
            "pos.order.line",
            [["order_id","=",order.id]],
            [],
        );
        return orderlines;
    },

    async _barcodeReceiptAction(code) {
        console.log("Code from action", code);
        
        const order = await this._getOrderByBarcode(code.code);

        if (!order) {
            this.dialog.add(AlertDialog, {
                title: "Order Not Found",
                body: `No order found for barcode: ${code.code}`,
            });
            return;
        }

        const lines = await this._getOrderLines(order);

        if (!lines || lines.length === 0) {
            this.notification.add(_t("No Order Lines Found!"), { type: "warning" });
            return;
        }

        this.dialog.add(ReturnOrderDialog, {
            title: "Return / Exchange Order",
            order: order,
            lines: lines,
            confirm: async ({ refundLines, exchangeLines, exchangeType, note }) => {
                const currentOrder = this.pos.getOrder();

                if (order.partner_id) {
                    const partner = Array.isArray(order.partner_id)
                        ? this.pos.models["res.partner"].get(order.partner_id[0])
                        : order.partner_id;
                    if (partner) currentOrder.setPartner(partner);
                }

                if (refundLines.length) {
                    await this._processReturnLines(refundLines, currentOrder, note);
                    currentOrder.nf_return_exchange_reason = `${note}` || '';
                    currentOrder.setScreenData({ name: "PaymentScreen" });
                    this.pos.navigate("PaymentScreen", {
                        orderUuid: currentOrder.uuid,
                    });
                    return;
                }

                if (exchangeLines.length) {
                    await this._processExchangeLines(
                        exchangeLines,
                        currentOrder,
                        exchangeType,
                        note
                    );
                    currentOrder.nf_return_exchange_reason = `${note}` || '';
                    this.notification.add(
                        _t("Exchange lines added successfully in current order."),
                        { type: "info" }
                    );
                }
            },
            cancel: () => { },
        });
    },

    async _processReturnLines(selectedLines, currentOrder, note) {
        const orderLines = [];

        for (const line of selectedLines) {
            const product = line.product_id;

            if (!product) {
                console.warn("Product not found:", line.product_id);
                continue;
            }

            const originalLine = line._originalLine;
            currentOrder.nf_return_exchange_reason = note || '';

            const vals = {
                product_id: product,
                product_tmpl_id: product.product_tmpl_id,
                qty: -(line.refund_qty),
                price_unit: line.price_unit,
                discount: line.discount || 0,
                tax_ids: originalLine?.tax_ids?.map(
                    (tax) => ["link", tax]
                ) || [],
                refunded_orderline_id: originalLine || null,
                attribute_value_ids: originalLine?.attribute_value_ids?.map(
                    (attr) => ["link", attr]
                ) || []
            };
            if (vals.refunded_orderline_id === null) {
                continue;
            }
            else{
                const orderLine = await this.pos.addLineToCurrentOrder(vals);
                if (orderLine) orderLines.push(orderLine);
            }
        }
        currentOrder.is_refund = true;
        return orderLines;
    },

    async _processExchangeLines(exchangeLines, currentOrder, exchangeType, note) {
        const orderLines = [];

        for (const line of exchangeLines) {
            const product = line.product_id;

            if (!product) {
                console.warn("Product not found:", line.product_id);
                continue;
            }

            const originalLine = line._originalLine;
            currentOrder.nf_return_exchange_reason = note || '';

            const returnVals = {
                product_id: product,
                product_tmpl_id: product.product_tmpl_id,
                qty: -(line.exchange_qty),
                price_unit: line.price_unit,
                discount: line.discount || 0,
                tax_ids: originalLine?.tax_ids?.map(
                    (tax) => ["link", tax]
                ) || [],
                refunded_orderline_id: originalLine || null,
                attribute_value_ids: originalLine?.attribute_value_ids?.map(
                    (attr) => ["link", attr]
                ) || []
            };

            const returnLine = await this.pos.addLineToCurrentOrder(returnVals);
            if (returnLine) orderLines.push(returnLine);

            if (exchangeType === "same") {
                const exchangeVals = {
                    product_id: product,
                    product_tmpl_id: product.product_tmpl_id,
                    qty: line.exchange_qty,
                    price_unit: line.price_unit,
                    discount: line.discount || 0,
                    tax_ids: originalLine?.tax_ids?.map(
                        (tax) => ["link", tax]
                    ) || [],
                    attribute_value_ids: originalLine?.attribute_value_ids?.map(
                        (attr) => ["link", attr]
                    ) || []
                };

                const exchangeLine = await this.pos.addLineToCurrentOrder(exchangeVals);
                if (exchangeLine) orderLines.push(exchangeLine);
            }
        }
        currentOrder.is_exchange = true;
        return orderLines;
    },
});