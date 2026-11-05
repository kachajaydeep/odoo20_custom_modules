import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";

patch(PaymentScreen.prototype, {  
    setup(){
        super.setup(...arguments);
        this.orm = useService('orm');
    },
    async validateOrder(isForceValidate) {
        let order = this.pos.getOrder();
        let lines = order.getOrderlines();
        const user_id = this.pos.user;
        const analytic_group = await user.hasGroup("analytic.group_analytic_accounting")
        
        if(!analytic_group){
            await super.validateOrder(isForceValidate);
            return
        }
        
        if(this.pos.config.nf_analytic_account_id) {
                order.nf_analytic_account_id = this.pos.config.nf_analytic_account_id;
                // order.session_id.nf_analytic_account_id = this.pos.config.nf_analytic_account_id;
                for (let line of lines){
                    line.setAccountAnalytic(this.pos.config.nf_analytic_account_id);
                }
            }
        await super.validateOrder(isForceValidate);
    }
})
