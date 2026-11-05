import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {
    async processServerData() {
        await super.processServerData(...arguments);
        try {
            const service = this.env.services["nf_pos_shortcut_service"];
            if (service) service.register(this);
        } catch (e) {
            console.warn("[NF Shortcuts] Init error:", e);
        }
    },
});