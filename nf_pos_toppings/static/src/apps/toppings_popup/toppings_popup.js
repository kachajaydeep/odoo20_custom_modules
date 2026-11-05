import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { Component, onMounted, useRef, proxy } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";

export class ToppingsPopup extends Component {
    static template = "nf_pos_toppings.ToppingsPopup";
    static components = { Dialog, ProductCard };

    setup() {
        this.pos = usePos();
        this.product_topping_ids = this.props.product_obj.topping_group_ids.flatMap(group =>
            group.product_topping_ids
        );

        this.state = proxy({
            toppings: [...this.props.product_toppings] || [],
            product: this.props.product_obj || null,
            toppings_obj:Object.fromEntries(this.props.product_obj?.topping_group_ids.map((elem) => [elem.id, 0])),
            products_obj: Object.fromEntries(this.product_topping_ids.sort((a,b) => a - b).map((elem) => [elem.id, 0]))
        });
    }

    getProductImage(product) {
        return product.getImageUrl();
    }

    onClickProduct({ product, combo_item }, ev){
        if (this.state.products_obj[product.id]){
            this.state.products_obj[product.id] = 0;
        }
        else{
            this.state.products_obj[product.id] = 1;
        }
    }

    confirm(products_obj){
        const selectedId = Object.keys(products_obj).filter(id => products_obj[id]);
        this.getSelectedComboItems(selectedId);
        const payload = this.props.getPayload(this.getSelectedComboItems(selectedId));
        this.props.close();
    }

    getSelectedComboItems(selectedId){
        const obj = selectedId.map(id => this.pos.models["product.product"].get(Number(id)));
        return obj;
    }
    closePopup(){
        this.props.close();
    }
}