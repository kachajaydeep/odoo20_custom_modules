import { DataServiceOptions } from "@point_of_sale/app/models/data_service_options";
import { patch } from "@web/core/utils/patch";

patch(DataServiceOptions.prototype, {
    get databaseTable() {
        return {
            ...super.databaseTable,
            "nf.tailor.order": {
                key: "id",
                condition: (record) => {
                    return !(record.pos_order_id?.finalized && typeof record.pos_order_id.id === "number")
                },
                serialize: (record) => {
                    if (!record.write_date || isNaN(new Date(record.write_date))) {
                        record.write_date = new Date().toISOString();
                    }
                    return record;
                },
            },
            // "mrp.bom":{
            //     key: "id",
            //     condition:record => true,
            //     serialize: record => record
            // },
            // "mrp.bom.line":{
            //     key: "id",
            //     condition:record => true,
            //     serialize: record => record
            // },
            "nf.measurement.line": {
                key: "id",
                condition: (record) => true,
            },
            "nf.measurement": {
                key: "uuid",
                condition: (record) => true,
            },
        };
    },
    get dynamicModels() {
        return [...super.dynamicModels, 
            "nf.tailor.order",
            "nf.measurement.line",
            "nf.measurement",
            // "mrp.bom",
            // "mrp.bom.line",
        ];
    },
    get prohibitedAutoLoadedModels() {
        return [...super.prohibitedAutoLoadedModels, 
            "nf.tailor.order",
            "nf.measurement.line",
            "nf.measurement",
            // "mrp.bom",
            // "mrp.bom.line",
        ];
    },
});