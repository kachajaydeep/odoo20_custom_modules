import {
    patch
} from "@web/core/utils/patch";
import {
    PosStore
} from "@point_of_sale/app/services/pos_store";
import {
    _t
} from "@web/core/l10n/translation";

patch(PosStore.prototype, {
    async pay() {
        let orderlines = this.getOrder().getOrderlines();

        if (!this.config.nf_restrict_discount) {
            await super.pay(...arguments);
            return;
        }
        for (let line of orderlines) {
            let nf_discount = line.getDiscount();
            let isValid = await this.getOrder().nfsetDiscount(line, nf_discount);

            if (isValid === false) {
                this.notification.add(_t("The applied discount exceeds the maximum allowed for this product."), {
                    type: "danger",
                });
                return;
            }
        }
        await super.pay(...arguments);
    },
});