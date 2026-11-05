import {ControlButtons} from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import {NfSaleOrderPopup} from "@nf_pos_create_saleorder/app/popups/nf_create_saleorder_popup";
import {ConfirmationDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {TextInputPopup} from "@point_of_sale/app/utils/input_popups/text_input_popup";
import {makeAwaitable} from "@point_of_sale/app/store/make_awaitable_dialog";
import {patch} from "@web/core/utils/patch";
import {AlertDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {_t} from "@web/core/l10n/translation";

patch(ControlButtons.prototype, {
    async saleOrderBtnClicked() {
        var self = this;
        if (
            this.pos.get_order() &&
            this.pos.get_order().get_orderlines() &&
            this.pos.get_order().get_orderlines().length > 0
        ) {
            if (self.pos.get_order().get_partner()) {
                const payload = await makeAwaitable(
                    this.dialog,
                    NfSaleOrderPopup,
                    {}
                );
                console.log("payload", payload);

                const {confirmed} = await this.dialog.add(ConfirmationDialog, {
                    title: _t("Sale Order Created!"),
                    body: _t(" Sale Order Created with name of " + payload),
                    confirmText: _t("Okay"),
                    cancelText: _t("Cloase"),
                });

                console.log("confirmed", confirmed);
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
        var self = this;
        var CurruntOrder = this.pos.get_order();
        const payload = await makeAwaitable(this.dialog, TextInputPopup, {
            title: _t("Selection"),
            placeholder: _t("Selection name"),
        });
        console.log('payload',payload);
        
        var SectionProduct = self.pos.models['product.product'].filter(x => x.nf_demo_product_for_sale_section)[0];
        if (CurruntOrder.get_selected_orderline() && CurruntOrder.get_selected_orderline().nf_section) {
            CurruntOrder.get_selected_orderline().set_orderline_section(payload);
        } else {

             await this.pos.addLineToCurrentOrder({
                product_id: SectionProduct,
                qty: 1,
                
            }, {nf_section: payload});

            // var line = new Orderline(
            //     { env: self.env },
            //     {
            //         pos: self.pos,
            //         order: CurruntOrder,
            //         product: SectionProduct,
            //     }
            // );
            // line.set_orderline_section(payload);
            // await CurruntOrder.add_orderline(line);
        }
    },
});
