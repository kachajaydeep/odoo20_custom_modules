import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, {
    get nf_is_gretore(){
        const base_pricelist = this.line.config.pricelist_id;
        const order_pricelist = this.line.order_id.pricelist_id
        if ( this.line.config.nf_pos_enable_dicsounted_price_on_cart ){
            const default_sale_price = this.line.getProduct().getPrice(base_pricelist, this.line.qty,);
            const offer_price = this.line.getProduct().getPrice(order_pricelist, this.line.qty,);
            if (base_pricelist && base_pricelist.id != order_pricelist.id  ){
                if ( default_sale_price == offer_price ){ return true; }
                else{ return default_sale_price > offer_price; }
            }
            else
            {
                return default_sale_price > offer_price;
            }
        }
        else
        {
            return false;
        }   
    },

    get custom_discount(){
        let result = 0;
        let total_disc = 0;
        if (this.line.config.pricelist_id && this.line.config.pricelist_id.id != this.line.order_id.pricelist_id.id  ){
            let default_sale_price = this.line.getProduct().getPrice(this.line.config.pricelist_id, this.line.qty,);
            const sale_price = default_sale_price;
            let offer_price = this.line.getProduct().getPrice(this.line.order_id.pricelist_id, this.line.qty,);
            
            if ( sale_price == offer_price ){                
                offer_price = this.line.price_unit * this.line.qty;
                total_disc = ((sale_price - offer_price) / sale_price * 100);
                
                if (this.line.config.nf_pos_enable_discounted_price_in_receipt && total_disc) {                                        
                    if (total_disc < 100 && total_disc > 0) {
                        result = parseFloat(total_disc.toFixed(1)) || 0;
                    }
                }
            }
            else
            {
                total_disc = ((sale_price - offer_price) / sale_price * 100);
                if (this.line.config.nf_pos_enable_discounted_price_in_receipt) {
                    if (total_disc < 100 && total_disc > 0) {
                        result = parseFloat(total_disc.toFixed(2));
                    }
                }
            }
        }
        return result
    },

    get nf_product_price(){
        const product = this.line.getProduct();
        return product.getTaxDetails().raw_total_included || 0.00;
    }
})