import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { session } from "@web/session";

const INPUT_KEYS = new Set(
    ["Delete", "Backspace", "+1", "+2", "+5", "+10", "+20", "+50"].concat(
        "0123456789+-.,".split("")
    )
);
const CONTROL_KEYS = new Set(["Enter", "Esc"]);
const ALLOWED_KEYS = new Set([...INPUT_KEYS, ...CONTROL_KEYS]);

patch(ProductScreen.prototype, {
    setup(){
        super.setup(...arguments)
        var self = this;
        this.numberBuffer._onInput = function (keyAccessor) {
            return (manualCapture = false) => {
            if (
                manualCapture ||
                session.test_mode ||
                (!manualCapture && this.eventsBuffer.length <= 2)
            ) {
                for (const event of this.eventsBuffer) {
                    if ([ "Backspace", "Delete"].includes(keyAccessor(event)) && self.pos.getCashier() && self.pos.getCashier().nf_disable_qty_button){
                        this.eventsBuffer = [];
                        return;
                       
                    }else{
                         if (!ALLOWED_KEYS.has(keyAccessor(event))) {
                            this.eventsBuffer = [];
                            return;
                        }
                    }
                }
                for (const event of this.eventsBuffer) {
                    this._handleInput(keyAccessor(event));
                    event.preventDefault();
                    event.stopPropagation();
                }
            }
            this.eventsBuffer = [];
        };
            
        }
    },
    getNumpadButtons() {
        var results = super.getNumpadButtons(...arguments)
        
        for (let i = 0; i < results.length; i++) {
            var button = results[i];
            
            if (button.value == "Backspace"){
                button['disabled'] = this.pos.getCashier() && this.pos.getCashier().nf_hide_delete_order_button || false
            } else if(button.value == "price"){
                button['disabled'] = this.pos.getCashier() && this.pos.getCashier().nf_disable_price_button || false
            } else if(button.value == "quantity"){
                button['disabled'] = this.pos.getCashier() && this.pos.getCashier().nf_disable_qty_button || false
            } else if(button.value == "discount"){
                button['disabled'] = this.pos.getCashier() && this.pos.getCashier().nf_disable_discount_button || false
            } else if(button.value == "-"){
                button['disabled'] = this.pos.getCashier() && this.pos.getCashier().nf_disable_plus_minus_button || false
            }
            
        }
        
        if ( this.pos.getCashier() && this.pos.getCashier().nf_hide_numpad_buttons ){
            return [] 
        }else{
            return results
        }

    }
})