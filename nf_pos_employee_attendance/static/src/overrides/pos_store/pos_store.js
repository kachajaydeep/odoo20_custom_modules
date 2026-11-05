import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {
    async setup() {
        await super.setup(...arguments);

        this.data.connectWebSocket(
            "nf_break_time_notification",
            (message) => {
                this._notifyEmployee(
                    message,
                    _t("It's time to take a break!"),
                    "warning"
                );
            }
        );

        this.data.connectWebSocket(
            "nf_checkout_notification",
            (message) => {
                this._notifyEmployee(
                    message,
                    _t("Your 8-hour shift is over. You can leave now."),
                    "success"
                );
            }
        );
    },

    _notifyEmployee(message, text, type = "warning") {
        const cashier = this.getCashier();
        if (!cashier) {
            return;
        }

        if (cashier.id === message.payload.employee_id) {
            this.notification.add(text, {
                type,
                sticky: true,
            });
        }
    },

    nf_check_in_send_notification() {
        this.notification.add(
            _t("Check-in successful"),
            {
                type: "success",
            }
        );
    },
});