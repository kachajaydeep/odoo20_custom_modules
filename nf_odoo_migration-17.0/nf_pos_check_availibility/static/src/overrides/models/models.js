
/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { Order, Orderline, Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(Order.prototype, {
    async pay() {
        if (this.pos.config.nf_check_stock){
            if (this.pos.config.nf_allow_to_sale){
                super.pay()
            } else {
                var allow = true
                const orderlines = this.get_orderlines()
                for (let i=0; i <  orderlines.length; i++){
                    const line = orderlines[i]
                    if (!line.stock_availibility){
                        allow = false
                    }
                }
                if (allow){
                    super.pay()
                }else{
                    this.env.services.popup.add(ErrorPopup,  {
                        title: _t("Stock Warning !"),
                        body: _t( "Stock is not available!" ),
                    });
                }
            }
        }else{
            super.pay()
        }
    }
})
patch(Orderline.prototype, {
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.stock_availibility = undefined;
    },
    getDisplayClasses() {
        var res = super.getDisplayClasses()
        res['is_available'] = this.stock_availibility === true ? 'is_available' : ''
        res['is_not_available'] = this.stock_availibility === false ? 'is_not_available' : ''
        console.log('res',res);
        return res
    }

})