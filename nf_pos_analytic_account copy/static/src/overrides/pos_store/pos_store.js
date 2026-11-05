import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";
import { user } from "@web/core/user";

patch(PosStore.prototype, {
    async validateOrder(args = {}) {
        let order = this.getOrder();
        let lines = order.getOrderlines();
        const user_id = this.user;
        const analytic_group = await user.hasGroup("analytic.group_analytic_accounting")
        
        if(!analytic_group){
            await super.validateOrder(...arguments);
            return
        }
        
        if(this.config.nf_analytic_account_id) {
                order.nf_analytic_account_id = this.config.nf_analytic_account_id;
                // order.session_id.nf_analytic_account_id = this.config.nf_analytic_account_id;
                for (let line of lines){
                    line.setAccountAnalytic(this.config.nf_analytic_account_id);
                }
            }
        await super.validateOrder(...arguments);
    }
})