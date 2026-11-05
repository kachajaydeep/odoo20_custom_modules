
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { NfSaleOrderPopup } from "@nf_pos_create_saleorder/app/popups/nf_create_saleorder_popup";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { TextInputPopup } from "@point_of_sale/app/components/popups/text_input_popup/text_input_popup";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

patch(ControlButtons.prototype, {
    setup() {
        super.setup(...arguments);
        this.notification = useService("notification");
    },

    async saleOrderBtnClicked() {
        const self = this;
        if (
            this.pos.getOrder() &&
            this.pos.getOrder().getOrderlines() &&
            this.pos.getOrder().getOrderlines().length > 0
        ) {
            if (self.pos.getOrder().getPartner()) {
                const payload = await makeAwaitable(
                    this.dialog,
                    NfSaleOrderPopup, {}
                );
            } else {
                await this.dialog.add(AlertDialog, {
                    title: _t("Customer not Found!"),
                    body: _t("Please Select Customer to Create Sale Order."),
                });
                return false;
            }
        } else {
            await this.dialog.add(AlertDialog, {
                title: _t("Empty Order"),
                body: _t("Please Select Products to Create Sale Order."),
            });
            return false;
        }
    },
    async nfAddSectionClicked() {
        const self = this;
        const CurruntOrder = this.pos.getOrder();
        const payload = await makeAwaitable(this.dialog, TextInputPopup, {
            title: _t("Selection"),
            placeholder: _t("Selection name"),
        });
        
        const SectionProduct = self.pos.models['product.template'].filter(x => x.nf_demo_product_for_sale_section)[0];

        if(!SectionProduct.uom_id){
            const uom = self.pos.models['uom.uom'].find(x => x.id == 1);
            if(uom){ SectionProduct.uom_id = uom; }
        }

        if (CurruntOrder.getSelectedOrderline() && CurruntOrder.getSelectedOrderline().nf_section) {
            if (payload) {
                CurruntOrder.getSelectedOrderline().nf_section = payload;
            }
        } else {
            if (payload) {

                await this.pos.addLineToCurrentOrder({
                    product_id: SectionProduct.product_variant_ids[0],
                    product_tmpl_id: SectionProduct,
                    qty: 0,
                    price_unit: 0,
                }, {
                    nf_section: payload,
                    merge: false
                });

                CurruntOrder.getSelectedOrderline().nf_section = payload;
            }
        }
    },
});