import {
    OrderSummary
} from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";
import {
    patch
} from "@web/core/utils/patch";
import {
    _t
} from "@web/core/l10n/translation";
import {
    useService
} from "@web/core/utils/hooks";

patch(OrderSummary.prototype, {
    setup() {
        super.setup();
        this.notification = useService("notification");
    },

    async _setValue(val) {
        await super._setValue(...arguments);

        if (!this.pos.config.nf_restrict_discount) {
            return false
        }

        const { numpadMode } = this.pos;
        let selectedLine = this.currentOrder.getSelectedOrderline();

        if (selectedLine) {
            let nf_discount = selectedLine.getDiscount();
            if (numpadMode === "discount" && val !== "remove") {
                let nf_set_discount = await this.currentOrder.nfsetDiscount(
                    selectedLine,
                    nf_discount
                );

                if (nf_set_discount === false) {
                    this.notification.add(_t("The applied discount exceeds the maximum allowed for this product."), {
                        type: "danger",
                    });
                }
            }
        }
    }
});