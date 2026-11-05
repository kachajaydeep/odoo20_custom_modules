import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    get idleTimeout() {
        super.idleTimeout;
        const is_enable = this.config.nf_enable_auto_lock;
        const timeout = this.config.nf_auto_lock_timeout;
        const saverTimeout  = is_enable ? timeout * 1000 : 300000;
        const loginTimeout  = is_enable ? saverTimeout + 60000 : 120000;

        return [
            {
                timeout: saverTimeout,
                action: () =>
                    this.router.currentScreen !== "PaymentScreen" &&
                    this.navigate("SaverScreen"),
            },
            {
                timeout: loginTimeout,
                action: () =>
                    this.router.currentScreen !== "LoginScreen" &&
                    this.navigate("SaverScreen"),
            },
        ];
    }
});