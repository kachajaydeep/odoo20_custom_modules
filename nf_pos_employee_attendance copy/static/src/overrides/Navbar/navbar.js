import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { Navbar } from "@point_of_sale/app/components/navbar/navbar";

patch(Navbar.prototype, {
    setup(){
        super.setup()
        this.orm = useService("orm");
    },
    
    async _checkOutCashier() {
        const cashier = this.pos.getCashier();
        if (!cashier) { return false; }
        try {
            await this.orm.call(
                "hr.employee",
                "nf_check_in_out_from_pos",
                [[cashier.id], false, false, true]
            );
            return true;
        } catch (error) {
            console.error("POS checkout failed:", error);
            return false;
        }
    },

    async showLoginScreen() {
        await this._checkOutCashier();

        this.notification.add(
            _t( "Check-out successfully" ),
            { type: "warning", }
        )
        return this.pos.showLoginScreen()
    },

    async showLoginScreenwitt_break(){
        await this._checkOutCashier();

        this.notification.add(
            _t( "Break start!" ),
            { type: "warning", }
        )

        return this.pos.showLoginScreen();
    }
})