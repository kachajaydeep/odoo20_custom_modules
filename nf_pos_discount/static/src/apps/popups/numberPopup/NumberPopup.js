import { patch } from "@web/core/utils/patch";
import { useProps, t } from "@odoo/owl";
import { NumberPopup } from "@point_of_sale/app/components/popups/number_popup/number_popup";
import { _t } from "@web/core/l10n/translation";

patch(NumberPopup.prototype, {
    setup() {
        super.setup();
        this.customProps = useProps({
            isInputSelected: t.boolean().optional(),
            is_custom_discount: t.boolean().optional(),
        });

        this.discount_type = "percentage";
    },
    setType() {
        this.discount_type = "amount";
    },
    confirm() {
        this.props.getPayload(this.getPayload());
        this.props.close();
    },
    getPayload() {
        
        if (this.discount_type == "amount") {
            return {
                discount_type: this.discount_type,
                amount: this.state.buffer,
            };
        } else {
            return this.state.buffer
        }
    },
});