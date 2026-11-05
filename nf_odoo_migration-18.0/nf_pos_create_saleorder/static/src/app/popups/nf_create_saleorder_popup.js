import {_t} from "@web/core/l10n/translation";
import {usePos} from "@point_of_sale/app/store/pos_hook";
import {makeAwaitable} from "@point_of_sale/app/store/make_awaitable_dialog";
import {Component, onMounted, useRef, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {Dialog} from "@web/core/dialog/dialog";

export class NfSaleOrderPopup extends Component {
    static template = "nf_pos_create_saleorder.NfSaleOrderPopup";
    static components = {Dialog};

    setup() {
        super.setup();
        this.pos = usePos();
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.Sale_oder_name = "";
        this.state = useState({
            selected_type: "quotation",
        });
    }
    isChecked() {
        return this.pos.config.nf_enable_create_saleorder
            ? "quotation"
            : "sale_order";
    }
    isValid() {
        return this.state.selected_type != "";
    }
    close() {
        this.props.close();
    }
    async confirm() {
        var self = this;
        var curruntOrder = self.pos.get_order();
        var OrderLines = curruntOrder.get_orderlines();
        var Partner = curruntOrder.get_partner();
        var SaleOrderState = this.state.selected_type;

        var orderlines = [];
        for (let i = 0; i < OrderLines.length; i++) {
            const each_line = OrderLines[i];

            var ProductId = each_line.get_product().id;
            var ProductName = each_line.get_product().display_name;
            var ProductQTY = each_line.qty;
            var ProductPrice = each_line.price_unit;
            var ProductDiscount = each_line.discount;

            if (each_line.get_product()?.nf_demo_product_for_sale_section) {
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

        var main_dic = {
            partner_id: Partner["id"],
            sale_order_lines: orderlines,
        };

        if (SaleOrderState == "quotation") {
            main_dic["quotation"] = true;
        }
        if (SaleOrderState == "sale_order") {
            main_dic["is_confirm"] = true;
        }

        var sale_order = await this.orm.call(
            "sale.order",
            "NfPosCreateSaleOrder",
            [[main_dic]]
        );
        if (sale_order.QuotationList && sale_order.QuotationList.length) {
            this.Sale_oder_name = sale_order.QuotationList[0].order_name;
        } else if (
            sale_order.saleOrderlist &&
            sale_order.saleOrderlist.length
        ) {
            this.Sale_oder_name = sale_order.saleOrderlist[0].order_name;
        }

        [...OrderLines].map((line) => curruntOrder.removeOrderline(line));

        this.props.getPayload();
        this.props.close();
        this.notification.add(_t("Successfully Sale Order Created"), 3000);
    }
    getPayload() {
        return this.Sale_oder_name || "";
    }
}
