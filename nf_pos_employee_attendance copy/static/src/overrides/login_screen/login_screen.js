import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { LoginScreen } from "@point_of_sale/app/screens/login_screen/login_screen";

patch(LoginScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
    },
    async selectCashier() {
        const result = await super.selectCashier(...arguments);
        const cashier = this.pos.cashier;

        if (this.pos.config.nf_enbale_check_in_out && cashier) {
            
            this.pos.nf_check_in_send_notification();
            await this.orm.call(
                "hr.employee",
                "nf_check_in_out_from_pos",
                [[cashier.id], false, true, false]
            );
        }
        return result;
    }
    
});
