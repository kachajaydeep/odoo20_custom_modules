import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { patch } from "@web/core/utils/patch";
import { ProductPopUp } from "@nf_pos_information/apps/popups/productpopup/productpopup"
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

patch(ProductCard.prototype, {
    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
    },
    async ButtonClicked(event){
        event.stopPropagation();
        const product = this.props.product;
        let currency_id = this.pos.config.currency_id
        
        await makeAwaitable(this.dialog, ProductPopUp, {
            'product': product,
            'currency':currency_id
        });
    },
})
