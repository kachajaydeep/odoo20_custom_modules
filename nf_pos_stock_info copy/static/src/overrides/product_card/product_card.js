import { proxy } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useBus } from "@web/core/utils/hooks";

patch(ProductCard, {
    props: {
        ...ProductCard.props,
    }
})
patch(ProductCard.prototype,{
    setup(){
        super.setup(...arguments)
        this.pos = usePos()
        
    
        this.state = proxy({
            available_quantity:this.getNfStock
        });

        useBus(this.env.bus, 'stock-updated', (ev) => {
            const payload = ev.detail || ev;
            const targetId = this.props.product.product_variant_id?.id || this.props.product.id;
            if (payload && payload.product_id === targetId) {
                if (payload.quantity !== undefined && payload.quantity !== null) {
                    this.state.available_quantity = payload.quantity;
                } else {
                    // this.state.available_quantity = this.getNfStock;
                    const quants = this.pos.models['stock.quant']?.filter(
                        (q) => (q.product_id?.id || q.product_id) === targetId
                    );
                    if (quants && quants.length > 0) {
                        this.state.available_quantity = quants.reduce((sum, q) => sum + q.quantity, 0);
                    }
                }
            } else if (!payload) {
                this.state.available_quantity = this.getNfStock;
            }
        });
    },

    get getNfStock() {
        const targetId = this.props.product.product_variant_id?.id || this.props.product.id;
        const all_stock = this.pos.models['stock.quant'].filter(
            (x) => (x.product_id?.id || x.product_id) == targetId
        );
        return all_stock.length ? all_stock[0].quantity : 0;
        return all_stock.reduce((total, q) => total + (q.quantity || 0), 0);
    },
    
    nf_click(event){
        event.stopPropagation()
       this.nf_click
    }
})