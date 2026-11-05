import { Component, proxy } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import {
    makeAwaitable,
    ask,
    makeActionAwaitable,
} from "@point_of_sale/app/utils/make_awaitable_dialog";

export class Measurement extends Component{
    static template = "nf_pos_tailor_management.Measurement";
    static components = { Dialog };
    setup(){
        this.pos = usePos();
        let order = this.pos.getOrder();
        this.orm = useService("orm");
        let partner_record = order.getPartner();
        
        this.action = useService("action");
        this.state = proxy({
            partner: partner_record,
            measurement:[...new Map(partner_record.measurement_ids.map(m => [m.id, m])).values()],
        })
        this.dialog = useService("dialog");
        
    }
    async getCutomerMeasurement(measure){
        const measurement = await makeActionAwaitable(
            this.action, "nf_pos_tailor_management.nf_Measurement_action", {
                props: { resId: measure.id },
                }
            );  
        const newMeasurement = await this.pos.data.read("nf.measurement",measurement.resIds)
        this.props.getPayload(newMeasurement)
        this.props.close();
    }

    async createMeasurement(){
        const created_measurement = await makeActionAwaitable(
            this.action, "nf_pos_tailor_management.nf_Measurement_action", {
                additionalContext:{
                    default_partner_id:this.pos.getOrder().getPartner().id,
                }
            }
        )
        const new_measurement = await this.pos.data.read("nf.measurement",created_measurement.resIds)
        this.pos.getOrder().getSelectedOrderline().setMeasurement(new_measurement[0])
        this.props.close();
    }

    closePopup(){
        this.props.close();
    }
}