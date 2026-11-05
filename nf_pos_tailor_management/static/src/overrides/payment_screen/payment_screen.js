import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { _t } from "@web/core/l10n/translation";

patch(PaymentScreen.prototype,{
    async onClickValidate(args = {}) {
        let order = this.pos.getOrder();
        let orderlines = order.getOrderlines();
        let partner = this.pos.getOrder().getPartner();

        for (let line of orderlines){
            if(line.nf_bom_component_ids.length){
                if(!line.nf_bom_component_ids.length){
                    this.pos.notification.add(
                        _t("Please! add the Bill of Material First!"),
                        {type: "warning",}
                    );  
                    return false;
                }
                else if(!partner){
                    this.pos.notification.add(
                        _t("Please! Select the Customer First!"),
                        {type: "warning",}
                    );  

                    return false;
                }
                else if(!line.nf_measurement_id){
                    this.pos.notification.add(
                        _t("Please! Choose Measurement First!"),
                        {type: "warning",}
                    );  

                    return false;
                }
                else if(!line.nf_delivery_date){
                    this.pos.notification.add(
                        _t("Please! Choose the Delivery Date First!"),
                        {type: "warning",}
                    );  
                    return false;
                }
                else{
                    const delivery_date= line.nf_delivery_date;
                    const dateStr = line.nf_measurement_id.create_date;
                    const date = new Date(dateStr);
                    const orderdate = date.toISOString().split("T")[0];
                    const bom = line.nf_bom_component_ids[0].nf_mrp_bom_id;
                    const component = line.nf_bom_component_ids.find(c => c.bom_id);
                    const tailor_order = await this.pos.data.models["nf.tailor.order"].create({
                        name: "New",
                        bom_id: component.bom_id || false,
                        company_id: this.pos.company,
                        customer_id: partner || false,
                        delivery_date: delivery_date,
                        order_date: orderdate,
                        product_id: line.product_id || false,
                        measurement_id: line.nf_measurement_id || false,
                        pos_order_id: order || false,
                        product_qty: line.qty,          // <-- add this
                        state: "confirmed",
                    });    
                }
            }
        }
        await super.onClickValidate(...arguments)
    }
})