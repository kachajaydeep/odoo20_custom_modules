import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

import { CategorySelector } from "@point_of_sale/app/components/category_selector/category_selector";



patch(CategorySelector.prototype,{
    setup(){
        super.setup(...arguments)
        this.pos = usePos()
    }
})

patch(ProductCard.prototype,{
    setup(){
        super.setup(...arguments)
        this.pos = usePos()
    }
})