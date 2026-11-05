import { Component, proxy } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import {_t} from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

export class DeliveryDate extends Component{
    static template = "nf_pos_tailor_management.DeliveryDate";
    static components = { Dialog };

    setup(){
        this.pos = usePos();
        this.notification = useService("notification");
        const orderline = this.pos.getOrder().getSelectedOrderline();
        this.state = proxy({
            deliveryDate:orderline?.nf_delivery_date || "",
        });
    }

    saveDeliveryDate(){
        const selectedDate = this.state.deliveryDate;

        if(selectedDate){
            const selectedNewDate = new Date(selectedDate);
            const currentDate = new Date();
            selectedNewDate.setHours(0, 0, 0, 0);
            currentDate.setHours(0, 0, 0, 0);

            if(selectedNewDate < currentDate){
                this.notification.add(
                    _t("Oops! Delivery date must be today or later."),
                    {type: "warning",}
                );

                return false
            }
            else{
                this.pos.getOrder().getSelectedOrderline().setDeliveryDate(selectedDate);
                // this.pos.getOrder().setShippingDate(selectedDate);
                this.pos.getOrder().shipping_date = selectedDate;
            }
            
            this.props.close();
        }
        else{
            return false;
        }
    }

    closePopup(){
        this.props.close();
    }
}