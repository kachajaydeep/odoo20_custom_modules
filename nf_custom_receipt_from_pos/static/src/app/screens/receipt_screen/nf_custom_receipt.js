/** @odoo-module **/

import { Component,xml,useSubEnv } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { formatCurrency } from "@web/core/currency";
import { generateQRCodeDataUrl } from "@point_of_sale/utils";
import { _t } from "@web/core/l10n/translation";


export class NfCustomReceipt extends Component {
    static template = "nf_custom_receipt_from_pos.NfCustomReceipt";

    setup() {
        this.pos = usePos();
        this.orm = useService("orm");

        const order = this.props.order || this.pos.getOrder();
        const data = this.props.data;
        const basic_receipt = this.props.basic_receipt;
        const currencyId = order?.currency?.id || this.pos.currency?.id;

        // Sub-env for env.utils.formatCurrency fallback
        useSubEnv({
            utils: {
                ...this.env.utils,
                formatCurrency: (v) => {
                    try {
                        return formatCurrency(v, currencyId);
                    } catch (_) {
                        return typeof v === "number" ? v.toFixed(2) : String(v || 0);
                    }
                }
            }
        });

        const config = (order && order.config) || this.pos.config;
        const templateId = Array.isArray(config.nf_receipt_template_id)
            ? config.nf_receipt_template_id[0]
            : config.nf_receipt_template_id;

        let templateRecord = null;
        if (this.pos.models && this.pos.models["nf.receipt.template"]) {
            const collection = this.pos.models["nf.receipt.template"];
            const all = typeof collection.getAll === "function" ? collection.getAll() : collection;
            if (all && all.find) {
                templateRecord = all.find((t) => t.id === templateId.id);
            }
        }

        if (templateRecord && templateRecord.nf_receipt_xml) {
            let rawXml = templateRecord.nf_receipt_xml.trim();
            
            // Check if rawXml contains the outer <t t-name="..."> wrapper and strip it
            rawXml = rawXml.replace(/^<t[^>]*>/i, "").replace(/<\/t>$/i, "").trim();

            try {
                const self = this;
                class DynamicReceipt extends Component {
                    static template = xml`${rawXml}`;

                    get receipt() {
                        const order = self.props.order || self.pos.get_order();
                        const data = self.props.data
                        
                        if (!order) {
                            return {
                                company: {},
                                orderlines: [],
                                paymentlines: [],
                                date: { localestring: "" }
                            };
                        }

                        // Exported print data as fallback/secondary info source
                        const exported = typeof order.export_for_printing === "function"
                            ? order.export_for_printing()
                            : {};

                        const hd = exported.headerData || {};
                        const companyRaw = hd.company || exported.company || self.pos.company || {};
                        
                        // 1. Company
                        const company = {
                            companyLogo:order.config.receiptLogoUrl || "",
                            basic_receipt:basic_receipt,
                            taxDetails:order.prices.taxDetails || "",
                            currencyDisplayPriceIncl:order.currencyDisplayPriceIncl || "",
                            priceExcl:order.priceExcl || "",
                            appliedRounding:order.appliedRounding,
                            totalDue:order.totalDue,
                            change:order.change,
                            showChange:order.showChange,
                            paymentLines:order.payment_ids,
                            getTotalDiscount:order.getTotalDiscount(),
                            name: companyRaw.name || "",
                            phone: companyRaw.phone || companyRaw.contact_address || "",
                            email: companyRaw.email || "",
                            website: companyRaw.website || "",
                            vat: companyRaw.vat || "",
                            street: companyRaw.street || "",
                            city: companyRaw.city || "",
                            zip:companyRaw.zip || "",
                            state_id:companyRaw.state_id,
                        };

                        // 2. Order Date localestring
                        let localestring = "";
                        const orderDate = order.date_order || exported.date;
                        if (orderDate) {
                            if (orderDate.toFormat) {
                                localestring = orderDate.toFormat("yyyy-MM-dd HH:mm:ss");
                            } else if (typeof orderDate.toLocaleString === "function") {
                                localestring = orderDate.toLocaleString();
                            } else {
                                localestring = String(orderDate);
                            }
                        } else {
                            localestring = new Date().toLocaleString();
                        }

                        // 3. Cashier
                        const cashier = order.cashier?.name 
                            || (order.get_cashier && order.get_cashier()?.name)
                            || hd.cashier 
                            || exported.cashier 
                            || "";

                        // 4. Orderlines
                        const lines = (order.getOrderlines ? order.getOrderlines() : (order.lines || []).slice()).map((l) => {
                        const productName = l.getFullProductName ? l.getFullProductName() : (l.productName || l.product_id?.display_name || "");
                        const qty = typeof l.get_quantity === "function" ? l.get_quantity() : (l.qty || 0);
                        const priceDisplay = typeof l.get_display_price === "function" ? l.getPrice() : (l.price_subtotal_incl || l.price || 0);
                        const unitPrice = typeof l.get_unit_display_price === "function" ? l.get_unit_display_price() : (l.price_unit || 0);

                            return {
                                id: l.id,
                                qty: qty,
                                productName: productName,
                                product_name_wrapped: [productName],
                                price_display: priceDisplay,
                                price: unitPrice,
                            };
                        });

                        // 5. Paymentlines
                        const payments = (order.payment_ids ? order.payment_ids : []).map((p) => {
                            return {
                                name: p.name || p.payment_method_id?.name || "",
                                amount: typeof p.getAmount === "function" ? p.getAmount() : (p.amount || 0),
                            };
                        });

                        // 6. Totals
                        const totalWithTax = order.priceIncl;
                        const totalWithoutTax = typeof order.get_total_without_tax === "function" ? order.get_total_without_tax() : (exported.total_without_tax || 0);
                        const change = typeof order.get_change === "function" ? order.get_change() : (exported.change || 0);
                        const totalDiscount = typeof order.getDiscount === "function" ? order.getDiscount() : (exported.total_discount || 0);
                        const new_coupon_info = order?.new_coupon_info;
                        
                        return {
                            order_name:order.name,
                            config_name:order.config.name,
                            companyRaw:companyRaw,
                            company: company,
                            name: order.name || exported.name || "",
                            date: { localestring: localestring },
                            cashier: cashier,
                            orderlines: lines,
                            paymentlines: payments,
                            total_with_tax: totalWithTax,
                            total_without_tax: totalWithoutTax,
                            change: change,
                            total_discount: totalDiscount,
                            order_shipping_date:order.shipping_date,
                            order_shipping: order.shipping_date
                            ? order.formatDateOrTime('shipping_date', 'date')
                            : '',
                            date_order:order.date_order,
                            date_order_formate:order.date_order ? order.formatDateOrTime('date_order') : '',
                            _IS_VAT:order.config._IS_VAT,
                            pos_reference:order.pos_reference,
                            receipt_header:order.config.receipt_header,
                            getCashierName:order?.getCashierName(),
                            tracking_number:order.tracking_number,
                            config_tracking_number:order.config.displayTrackingNumber,
                            config_displayBigTrackingNumber:order.config.displayBigTrackingNumber,
                            partner_id:order.partner_id,
                            presetDateTime:order?.presetDateTime,
                            preset_name:order.preset_id?.name,
                            new_coupon_info:new_coupon_info,
                            receipt_footer:order?.config?.receipt_footer,
                            ticket_code:order?.ticket_code,
                            point_of_sale_use_ticket_qr_code:order.company.point_of_sale_use_ticket_qr_code,
                            finalized:order?.finalized,
                        };
                    }

                    get qrCode() {
                        const order = self.props.order || self.pos.get_order();
                        const baseUrl = order.config._base_url;
                        const url = `${baseUrl}/pos/ticket/validate?access_token=${order.access_token}`;
                        return generateQRCodeDataUrl(url);
                    }

                     get header() {
                        const order = self.props.order || self.pos.get_order();
                        return {
                            company: order.company,
                            cashier: _t("Served by %s", this.order?.getCashierName()),
                            header: order.config.receipt_header,
                        };
                    }

                    getPortalURL() {
                        const order = self.props.order || self.pos.get_order();
                        return `${order.config._base_url}/pos/ticket`;
                    }
                }

                this.DynamicReceiptComponent = DynamicReceipt;
            } catch (e) {
                console.error("NfCustomReceipt: Failed to compile template:", e);
                this.DynamicReceiptComponent = null;
            }
        }
    }
}

NfCustomReceipt.props = {
    data: { type: Object },
    order: { type: Object, optional: true },
    formatCurrency: { type: Function, optional: true },
};
