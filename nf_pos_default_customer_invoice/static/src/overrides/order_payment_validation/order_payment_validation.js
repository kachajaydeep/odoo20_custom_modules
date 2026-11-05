import { patch } from "@web/core/utils/patch";
import OrderPaymentValidation from "@point_of_sale/app/utils/order_payment_validation";

patch(OrderPaymentValidation.prototype,{
    async validateOrder(isForceValidate = false) {
        const order = this.order;
        const partner = order.getPartner();
        if (partner && partner.nf_default_invoice) {
            order.to_invoice = true;
        }
        await super.validateOrder(isForceValidate);
    },

    async afterOrderValidation() {
        const order = this.order;
        const partner = order?.getPartner();
        const nf_direct_print_invoice = this.pos.config.nf_direct_print_invoice;

        await super.afterOrderValidation();

        if (partner?.nf_default_invoice && nf_direct_print_invoice) {
            try {
                if (!order.id) {
                    return;
                }

                const result = await this.pos.env.services.orm.read(
                    "pos.order",
                    [order.id],
                    ["account_move"]
                );

                if (result?.[0]?.account_move?.[0]) {
                    const invoiceId = result[0].account_move[0];
                    const orderData = await this.pos.env.services.orm.call(
                        "pos.config",
                        "getInvoicePrint",
                        [invoiceId]
                    );
                    printJS({ printable: orderData, type: "pdf", base64: true });
                }
            } catch (invoiceError) {
                console.error("Error printing invoice:", invoiceError);
            }
        }
    },
});