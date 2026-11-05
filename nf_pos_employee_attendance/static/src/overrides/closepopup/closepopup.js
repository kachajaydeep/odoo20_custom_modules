import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { ClosePosPopup } from "@point_of_sale/app/components/popups/closing_popup/closing_popup";

patch(ClosePosPopup.prototype, {
    setup(){
        super.setup(...arguments);
        this.orm = useService("orm");
        this.notification = useService("notification");
    },
    async closeSession() {
        const cashier = this.pos.getCashier()

        if (this.pos.config.nf_enbale_check_in_out && cashier) {
            await this.orm.call("hr.employee", "nf_check_in_out_from_pos", [
                [cashier.id], false, false, true,
            ]);
            this.notification.add(
                _t("Check-out successfully. Session Closed.."),
                { type: "success", }
            )
        }
        
        return super.closeSession(...arguments);
    }
})
