import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { ask } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { Component, proxy, markup } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";

export class NfSaleOrderPopup extends Component {
    static template = "nf_pos_create_saleorder.NfSaleOrderPopup";
    static components = {
        Dialog
    };

    setup() {
        super.setup();
        this.pos = usePos();
        this.orm = useService("orm");
        this.dialog = useService("dialog");
        this.notification = useService("notification");
        this.report = useService("report");
        this.Sale_order_name = "";
        this.Sale_order_id = 0;
        this.state = proxy({
            selected_type: "quotation",
        });
    }
    isChecked() {
        return this.pos.config.nf_enable_create_saleorder ?
            "quotation" :
            "sale_order";
    }
    isValid() {
        return this.state.selected_type != "";
    }
    close() {
        this.props.close();
    }
    async confirm() {
        let self = this;
        let curruntOrder = self.pos.getOrder();
        let OrderLines = curruntOrder.getOrderlines();
        let Partner = curruntOrder.getPartner();
        let SaleOrderState = this.state.selected_type;

        let orderlines = [];
        for (let i = 0; i < OrderLines.length; i++) {
            const each_line = OrderLines[i];

            let ProductId = each_line.getProduct().id;
            let ProductName = each_line.getProduct().display_name;
            let ProductQTY = each_line.qty;
            let ProductPrice = each_line.price_unit;
            let ProductDiscount = each_line.discount;

            if (each_line.getProduct()?.nf_demo_product_for_sale_section) {
                orderlines.push({
                    name: each_line.nf_section || "",
                    display_type: "line_section",
                });
            } else {
                orderlines.push({
                    product_id: ProductId,
                    name: ProductName,
                    product_uom_qty: ProductQTY,
                    price_unit: ProductPrice,
                    discount: ProductDiscount,
                });
            }
        }

        let main_dic = {
            partner_id: Partner["id"],
            sale_order_lines: orderlines,
        };

        if (SaleOrderState == "quotation") {
            main_dic["quotation"] = true;
        }
        if (SaleOrderState == "sale_order") {
            main_dic["is_confirm"] = true;
        }

        let sale_order = await this.orm.call(
            "sale.order",
            "NfPosCreateSaleOrder",
            [
                [main_dic]
            ]
        );

        if (sale_order.QuotationList && sale_order.QuotationList.length) {
            this.Sale_order_name = sale_order.QuotationList[0].order_name;
            this.Sale_order_id = sale_order.QuotationList[0].order_id;
        } else if (
            sale_order.saleOrderlist &&
            sale_order.saleOrderlist.length
        ) {
            this.Sale_order_name = sale_order.saleOrderlist[0].order_name;
            this.Sale_order_id = sale_order.saleOrderlist[0].order_id;
        }

        [...OrderLines].map((line) => curruntOrder.removeOrderline(line));

        this.props.getPayload();
        this.props.close();

        const confirmed = await ask(this.dialog, {
            body: markup(
                _t(
                    `Print Sale Order <style>.po-print-link { color: #1a73e8 !important; text-decoration: underline;} .po-print-link:hover {color: #0b47a1;text-decoration: underline;}</style><a class='po-print-link' href='/odoo/sales/%(id)s?model=sale.order' target='_blank'>%(name)s</a> ?`,
                    { id: this.Sale_order_id, name: this.Sale_order_name }
                )
            ),
            confirmLabel: _t("Print"),
            cancelLabel: _t("Cancel"),
        });
        if (confirmed) {
            return await this.report.doAction("sale.action_report_saleorder", [this.Sale_order_id]);
        }
        else {
            return this.Sale_order_name;
        }
    }

    getPayload() {
        return this.Sale_order_name || "";
    }
}