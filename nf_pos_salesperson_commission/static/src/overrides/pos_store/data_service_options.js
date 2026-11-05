import { DataServiceOptions } from "@point_of_sale/app/models/data_service_options";
import { patch } from "@web/core/utils/patch";

patch(DataServiceOptions.prototype, {
    get databaseTable() {
        return {
            ...super.databaseTable,
            "pos.commission.line": {
                key: "id",
                condition: (record) => { return !(record.order_id?.finalized && typeof record.order_id.id === "number")}
            },
        };
    },
    get dynamicModels() {
        return [...super.dynamicModels, "pos.commission.line"];
    },
    get pohibitedAutoLoadedModels() {
        return [...super.pohibitedAutoLoadedModels, "pos.commission.line"];
    },
})
