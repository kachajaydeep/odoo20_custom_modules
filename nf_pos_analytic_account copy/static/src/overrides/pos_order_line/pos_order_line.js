import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";


patch(PosOrderline.prototype,{
    setAccountAnalytic(account){
        this.nf_analytic_account_id = account
    }
})