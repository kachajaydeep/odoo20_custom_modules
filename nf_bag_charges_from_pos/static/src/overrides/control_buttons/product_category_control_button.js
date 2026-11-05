import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { NfProductCategoryPopup } from "@nf_bag_charges_from_pos/apps/product_category_popup/product_category_popup";
import { useService } from "@web/core/utils/hooks";

patch(ControlButtons.prototype, {
    setup() {
        super.setup(...arguments);
        this.dialog = useService("dialog");
    },

    async onClickOpenProductCategoryPopup() {
        const config = this.pos.config;

        if (!config?.nf_enable_bag_charges || !config?.nf_carry_bag_category_id) {
            return;
        }

        const catId = config.nf_carry_bag_category_id.id;

        try {
            const response = await fetch("/web/dataset/call_kw", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    jsonrpc: "2.0",
                    method: "call",
                    params: {
                        model: "pos.session",
                        method: "get_bag_templates_by_category",
                        args: [config.id, catId],
                        kwargs: {},
                    },
                }),
            });

            const json = await response.json();
            const templates = json?.result;

            if (!templates || templates.length === 0) {
                return;
            }

            this.dialog.add(NfProductCategoryPopup, {
                templates: templates,
            });

        } catch (e) {
            console.error("Bag RPC error →", e);
        }
    },
});
