import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductCard.prototype, {
    nf_click(event){
        event.stopPropagation()
        this.nf_state.nf_qty = this.getNfStock
    }
})

patch(ProductScreen.prototype, {
    setup() {
        super.setup(...arguments);
    },
})