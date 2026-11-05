import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";
import { patch } from "@web/core/utils/patch";

patch(OrderSummary.prototype, {
      _setValue(val) {
        const { numpadMode } = this.pos;
        const selectedLine = this.currentOrder.getSelectedOrderline();
        
        if(selectedLine && selectedLine.product_id.nf_is_topping === true){
            if(val === ""){
                const orderLines = this.currentOrder.getOrderlines();
                orderLines.filter(line => {
                    if(selectedLine.nf_child_orderline_id === line && line.price_unit !== 0){
                        line.price_unit -= selectedLine.product_id.lst_price
                    }
                })
                
            }
            super._setValue(...arguments);
        }
        // if(!selectedLine || selectedLine.product_id.topping_group_ids.length === 0){
        //     super._setValue(...arguments);
        //     return
        // }

        if (numpadMode === "quantity") {
            if(val === "remove"){
                
                if(selectedLine && !selectedLine.nf_child_orderline_id){
                    const orderLines = this.currentOrder.getOrderlines();
                    let linesToRemove = [];
                    
                    orderLines.filter(line => {
                    if (line.nf_child_orderline_id === selectedLine) {
                        linesToRemove.push(line);
                    }})
         
                    linesToRemove.map(line => {
                        this.currentOrder.removeOrderline(line);
                    });
                    this.currentOrder.removeOrderline(selectedLine);
                }
                else if(selectedLine && selectedLine.nf_child_orderline_id){
                    super._setValue(...arguments);
                }
            }
            else {
                   const order = this.currentOrder;
                    if (!order) return;

                    const selectedLine = order.getSelectedOrderline();
                    if (!selectedLine) return; 

                    const orderLines = this.currentOrder.getOrderlines();
                    const result = selectedLine.setQuantity(
                        val,
                        Boolean(orderLines?.length)
                    );
                    for (const line of orderLines) {
                        if (line.nf_child_orderline_id === selectedLine) {
                            line.setQuantity(val, true);
                        }
                    }
                }
        }
        else if (numpadMode === "discount" && val !== "remove") {
                if (selectedLine.combo_parent_id) {
                    selectedLine = selectedLine.combo_parent_id;
                }
                this.pos.setDiscountFromUI(selectedLine, val);
            } else if (numpadMode === "price" && val !== "remove") {
                this.setLinePrice(selectedLine, val);
        }
    }
})