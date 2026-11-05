/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { useComponent, useEffect, proxy } from "@odoo/owl";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";

patch(Orderline.prototype, {
    setup() {
        let self = this;
        super.setup();

        this.nf_state = proxy({
            togglebutton: false,
        });
        
        if (this.props.line.isSelected() && !self.env.services.pos.router.currentScreen() === "PaymentScreen") {        
            self.nf_state.togglebutton = true
        }

        useEffect(
            () => {
                const isSelected = this.props.line.isSelected();

                const currentScreen = this.env.services.pos.router?.currentScreen();
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
                this.env.services.pos.router?.currentScreen(),
            ]
        );
        setTimeout(() => {
            const padsElement = document.querySelector('.numpad');
            const isProductScreen = posmodel.router?.currentScreen() === "ProductScreen"
            if (padsElement?.classList && isProductScreen) {
                padsElement.classList.add('d-none');
                padsElement.classList.toggle('d-grid');
            }

        }, 10);

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
        let orderline = this.props.line;
        const padsElement = document.querySelector('.numpad');

        if (padsElement.classList) {
            padsElement.classList.toggle('d-none');
            padsElement.classList.toggle('d-grid');
        }
    },

    get nf_get_disount_price() {
        let price_after_discount = this.line.displayPrice;
        let discount_pice = (actualprice * this.line.qty) - price_after_discount;

        return actualprice * this.line.qty
    },

})


patch(OrderSummary.prototype, {
    clickLine(ev, orderline) {
        super.clickLine(...arguments);

        setTimeout(() => {
            const padsElement = document.querySelector('.numpad');
        
            if (padsElement && this.pos.router?.currentScreen() === "ProductScreen") {
                if (padsElement.classList) {
                    padsElement.classList.add('d-none');
                    padsElement.classList.toggle('d-grid');
                }
            }
        }, 10);

    },
})
