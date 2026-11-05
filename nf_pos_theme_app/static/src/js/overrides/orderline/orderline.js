/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { useComponent, useEffect, useState } from "@odoo/owl";

patch(Orderline.prototype, {
    setup() {
        var self = this;
        super.setup();

        this.nf_state = useState({
            togglebutton: false,
        });

        if (this.props.line.isSelected() && !self.props.line.order_id.getCurrentScreenData().name === "PaymentScreen") {
            self.nf_state.togglebutton = true
        }

        useEffect(
            () => {
                const isSelected = this.props.line.isSelected();
                const currentScreen = this.env.services.pos.router?.state.current;
                const isProductScreen = currentScreen === "ProductScreen";
 
                this.nf_state.togglebutton = isSelected && isProductScreen;
                const padsElement = document.querySelector('.numpad');
                if (padsElement && isProductScreen) {
                    padsElement.classList.add('d-none');
                    padsElement.classList.remove('d-grid');
                }                
            },
            () => [
                this.props.line.isSelected(),
                this.env.services.pos.router?.state.current,
            ]
        );
        // setTimeout(() => {
        //     const padsElement = document.querySelector('.numpad');
        //     const isProductScreen = posmodel.router?.state.current === "ProductScreen"
        //     if (padsElement?.classList && isProductScreen) {
        //         padsElement.classList.add('d-none');
        //         padsElement.classList.toggle('d-grid');
        //     }

        // }, 50);

    },
    get lineScreenValues() {
        const result = super.lineScreenValues;
        const lineModel = this.line;

        if (lineModel) {
            result['nf_get_disount_price'] = this.nf_get_discounted_price() || false;

            result['finalized'] = this?.line?.order_id?.finalized || false;
        }
        return result;
    },
    nfRemoveOrderLine(ev) {
        ev.stopPropagation();
        // let orderline = this.props.line;
        let orderline = posmodel.getOrder().getSelectedOrderline();
        if (orderline) {
            posmodel.getOrder().removeOrderline(orderline);
        }
    },
    nf_get_discounted_price() {
        let actualprice = this.priceIncl
        let price_after_discount = this.displayPrice

        let discount_pice = (actualprice * this.qty) - price_after_discount


        return actualprice * this.qty
    },

    // get nf_get_disount_price(){
    //     return this.env.utils.formatCurrency(
    //         this.props.line.nf_get_disount_price,
    //         this.currency
    //     )
    // },

    nfEditLine(ev) {
        ev.stopPropagation()
        var orderline = this.props.line;
        const padsElement = document.querySelector('.numpad');

        if (padsElement.classList) {
            padsElement.classList.toggle('d-none');
            padsElement.classList.toggle('d-grid');
        }
    },

    get nf_get_disount_price() {
        let actualprice = this.line.price_unit;
        let price_after_discount = this.line.displayPrice;

        let discount_pice = (actualprice * this.line.qty) - price_after_discount;

        return actualprice * this.line.qty
    },

})

// patch(Orderline, {
//     props: {
//         ...Orderline.props,
//         line: {
//             ...Orderline.props.line,
//             shape: {
//                 ...Orderline.props.line.shape,
//                 nf_get_disount_price: { type: Number, optional: true },
//                 finalized: { type: Boolean, optional: true },

//             },
//         },
//     },
// });
