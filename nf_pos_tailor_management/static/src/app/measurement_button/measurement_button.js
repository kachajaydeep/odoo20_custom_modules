import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { Measurement } from "@nf_pos_tailor_management/app/measurement_popup/measurement_popup";
import { DeliveryDate } from "@nf_pos_tailor_management/app/delivery_date_popup/delivery_date_popup"
import { MrpBom } from "@nf_pos_tailor_management/app/bill_material/mrp_bom_popup"


patch(ControlButtons.prototype,{
    async measurement() {        
      if(this.pos.getOrder().getPartner()){
        const payload = await makeAwaitable(this.dialog,Measurement,{});
        if(!this.pos.getOrder().getSelectedOrderline().nf_delivery_date){
          const popup = await makeAwaitable(this.dialog,DeliveryDate,{})
        }

        if(payload){
          this.pos.getOrder().getSelectedOrderline().setMeasurement(payload[0])
        }
      }
    },


    async deliveryDate(){
      const pay = await makeAwaitable(
          this.dialog,
          DeliveryDate,
          {}
        )
    },

    async UpdateBillOfMaterial(){
      let orderline = this.pos.getOrder().getSelectedOrderline();
      let product = orderline.product_id
      let bom_ids = product.bom_ids

      if(bom_ids){
        let payload = await makeAwaitable(
              this.dialog,
              MrpBom,
               {
                  bom_ids: bom_ids || [],
                  product: product,
              })
        if(payload){ 
          orderline.setMrpOrder(payload);
        }
      }
    }
});