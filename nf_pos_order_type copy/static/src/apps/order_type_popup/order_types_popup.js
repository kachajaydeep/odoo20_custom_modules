import { Component, proxy } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { _t } from "@web/core/l10n/translation";

export class OrderTypes extends Component{
    static template = "nf_pos_order_type.OrderTypes";
    static components = { Dialog };

    setup(){
        this.pos = usePos();
        this.dialog = useService("dialog");
        
        this.state = proxy({
            pos_order_type_ids : this.pos.config.nf_pos_order_type_ids || [],
        })
    }

    setOrder(order_type){
        if(!this.pos.getOrder().partner_id && order_type.is_delivery){
            this.env.services.notification.add(
                _t("No customer selected. Please select a customer to continue."),
                { type: "warning" }
            );

            return false
        }
        else if(this.pos.getOrder().partner_id && order_type.is_delivery){
            if(!this.pos.getOrder().partner_id.street && order_type.is_delivery){
                this.env.services.notification.add(
                    _t("Customer address is missing, Please add the customer address."),
                    {type: "warning",}
                );  
                return false
            }
        }
        this.pos.getOrder().set_pos_order(order_type);
        this.props.close();
    }
    closePopup(){
        this.props.close()
    }
}