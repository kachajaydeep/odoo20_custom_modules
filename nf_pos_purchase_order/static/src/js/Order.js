/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {

    _convert_pos_line_to_po_line: function (line) {

        let line_val = {
            product_id: line.product_id.id,
            price_unit: line.price_unit,
            product_qty: line.qty,
        };
        if (line.discount) {
            line_val['discount'] = line.discount
        }
        else {
            line_val['discount'] = 0
        }

        if (line.uom_id) {
            line_val['uom_id'] = line.uom_id
        }
        else {
            line_val['uom_id'] = line.product_id.uom_id.id
        }

        if (line.tax_ids) {
            line_val['taxes_id'] = line.tax_ids.ids;
        }
        return [0, 0, line_val];
    }
})