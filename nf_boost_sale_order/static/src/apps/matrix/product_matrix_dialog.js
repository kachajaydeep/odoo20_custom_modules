/** @odoo-module **/

import {_t} from "@web/core/l10n/translation";
import {patch} from "@web/core/utils/patch";
import {ProductMatrixDialog} from "@product_matrix/js/product_matrix_dialog";
import {proxy} from "@odoo/owl";

patch(ProductMatrixDialog.prototype, {
    setup() {
        super.setup();
        this.state = proxy({variant_qties: ""});
    },

    async _onChangeQty() {
        const variant_qties = this.state.variant_qties;
        const parts = variant_qties.trim().split(/\s+/);

        const sizeCount = this.props.rows[0].length - 1;
        
        // Create object
        const matrixObject = {};
        let i = sizeCount;

        while (i < parts.length) {
            const rowName = parts[i]; // get row name like 'wood'
            const rowValues = parts.slice(i + 1, i + 1 + sizeCount).map(Number); // next 5 values
            matrixObject[rowName] = rowValues;
            i += 1 + sizeCount;
        }
        
        for (let i = 0; i < this.props.rows.length; i++) {
            const element = this.props.rows[i];
            const key = element[0];
            console.log("\n\n key=>", key.name);

            const qty_value = matrixObject[key.name];
            // console.log('qty_value',qty_value);

            for (let j = 1; j < element.length; j++) {
                const ptev_id = element[j];
                console.log("j", typeof j, j);

                const qty = qty_value[j - 1];
                const input = document.querySelectorAll(
                    "input[ptav_ids='" + ptev_id.ptav_ids.join(",") + "']"
                );
                console.log(input);

                input[0].value = qty;
            }
        }
    },
});
