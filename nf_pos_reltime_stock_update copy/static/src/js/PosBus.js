import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {
    async setup() {
        await super.setup(...arguments);
        this.data.connectWebSocket("nf_update_stock", (notification) => {
            if (notification.config_id && this.config.id ){
                // console.log('--notificaion- >',notification);
                
                var stock = this.models['stock.quant'].filter((x) => (x.product_id?.id == notification.StockUpdate.product_id) && x.location_id.id ==this.pickingType.default_location_src_id.id );            
                
                // console.log('======>',stock, notification.StockUpdate);
                if (stock && stock.length){
                    if (stock && notification.StockUpdate.minus_quantity ){
                        const stock_qty = stock[0].quantity
                        if (stock_qty != notification.StockUpdate.quantity -notification.StockUpdate.minus_quantity || notification.StockUpdate.stock_adjustments ){
                            
                            stock[0].update({'quantity': notification.StockUpdate.quantity - notification.StockUpdate.minus_quantity,'available_quantity': stock[0].available_quantity - notification.StockUpdate.minus_quantity })
                            
                            var element = document.querySelector('.nf_product_qty'+notification.StockUpdate.product_id)
                            if (element) {
                                // Update the inner text of the first matching element
                                element.click()
                            }
                        }
                    }
                    else {
                        if(stock && notification.StockUpdate.stock_adjustments && this.getOrder().finalized === false){                        
                            
                            stock[0].update({'quantity': notification.StockUpdate.quantity,'available_quantity': notification.StockUpdate.quantity })
    
                            var element =  document.querySelector('.nf_product_qty'+ notification.StockUpdate.product_id)
                            if (element ) {
                                // Update the inner text of the first matching element
                                element.click()
                            }
                        }
                    }
                }
                else {
                    var create_dic = notification.StockUpdate
                    create_dic['location_id'] = this.models['stock.location'].get(notification.StockUpdate.location_id)
                    create_dic['product_id'] = this.models['product.product'].get(notification.StockUpdate.product_id)
                    this.models['stock.quant'].create(create_dic)
                    
                    var element =  document.querySelector('.nf_product_qty'+notification.StockUpdate.product_id.id)
                    if (element ) {
                        // Update the inner text of the first matching element
                        element.click()
                    }
                }
            }
        });
    },
    async addLineToCurrentOrder(vals, opts = {}, configure = true) {
        var result = await super.addLineToCurrentOrder(vals, opts, configure);
        var line = this.getOrder().getSelectedOrderline()    
        if (line){
            var dic = {
                    location_id: this.pickingType.default_location_src_id.id,
                    product_id: line.product_id.id,
                    minus_quantity: line.qty,
                    config_id:this.config.id
            }

            await this.data.call("pos.config", "send_notification", [[], dic]);
        
            var element = document.querySelector('.nf_product_qty'+ line.product_id.id)
            if(element){
                element.click()
            }
        }         
        return result
    },
});