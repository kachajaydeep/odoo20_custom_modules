import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { ProductImagePopup } from "@nf_pos_image_preview/app/popups/imagePopup/imagePopup";

patch (ProductCard.prototype, {
    setup(){
        this.dialog = useService("dialog");
    },
    async ImageButtonClicked(event){
        event.stopPropagation();
        let product =  this.props.product;
        await makeAwaitable(this.dialog, ProductImagePopup, {
            'product': product
        })
    }
})