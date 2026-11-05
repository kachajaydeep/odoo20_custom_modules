import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    get quantityForOrderline() {
        return this.lines.reduce((total_qty, line) => {
            if (line.qty > 0 && !line.combo_parent_id) {
                total_qty += line.qty;
            }
            this.nf_product_count = total_qty;
            return total_qty;
        }, 0);
    },
    get orderlineCount() {
        return this.lines.reduce((total_line, line) => {
            if (line && !line.combo_parent_id) {
                total_line += 1;
            }
            this.nf_line_count = total_line;
            return total_line;
        }, 0);
    }
})