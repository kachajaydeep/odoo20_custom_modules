import {
    PosOrder
} from "@point_of_sale/app/models/pos_order";
import {
    patch
} from "@web/core/utils/patch";
import {
    _t
} from "@web/core/l10n/translation";

patch(PosOrder.prototype, {
    async nfsetDiscount(line, nf_discount) {
        if (nf_discount) {
            let product_tmpl = line.product_id.product_tmpl_id;
            let product_tmpl_price = product_tmpl.list_price;
            if (product_tmpl.nf_discount_type == "percentage") {
                let product_percentage_discount = product_tmpl.nf_discount_limit;
                if (product_percentage_discount < nf_discount && product_percentage_discount != 0) {
                    return false
                }
            } else {
                let product_fixed_discount = product_tmpl.nf_discount_limit * line.getQuantity();
                let product_discount = (product_tmpl_price * nf_discount * line.getQuantity()) / 100;

                if ((product_fixed_discount < product_discount) && (product_fixed_discount !== 0)) {
                    return false
                }
            }

            let categories = line.product_id.product_tmpl_id.pos_categ_ids;

            for (let category of categories) {
                let category_discount = category.nf_discount_limit;
                if (category.nf_discount_type == "percentage") {
                    if (category_discount && category_discount < nf_discount) {
                        return false
                    }
                } else {
                    let product_discount = (product_tmpl_price * nf_discount * line.getQuantity()) / 100;

                    if (category_discount < product_discount && category_discount !== 0) {
                        return false
                    }
                }
            }
        }
    }
})