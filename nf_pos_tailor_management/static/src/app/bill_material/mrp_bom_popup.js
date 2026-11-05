import { Component, proxy } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { makeActionAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

export class MrpBom extends Component{
    static template = "nf_pos_tailor_management.MrpBom";
    static components = { Dialog };

    setup(){
        this.pos = usePos();
        this.action = useService("action");
        this.state = proxy({
            bom_ids:[...this.props.bom_ids],
            product:this.props.product,
        })
    }

    async posOrderPopup(material){    
        let bom_line_ids = material.bom_line_ids;

        if (bom_line_ids && bom_line_ids.length > 0) {
            const ids = bom_line_ids
            .map(line => {
                if (typeof line === "number") return line;
                if (line && typeof line.id === "number") return line.id;
                return null;
            })
            .filter(id => Number.isInteger(id));
        
            await this.pos.data.read("mrp.bom.line", ids);

            bom_line_ids = ids
            .map(id => this.pos.data.models["mrp.bom.line"].get(id))
            .filter(line => line);
        }
     
        const record = await makeActionAwaitable(
            this.action,
            "nf_pos_tailor_management.nf_pos_bill_material_action",
            {
                additionalContext:{
                default_nf_bom_component_ids: bom_line_ids
                    .filter(line => line.product_id)
                    .map(line => [0,0,{
                        product_id: line.product_id.id,
                        product_qty: line.product_qty,
                        bom_id:line.bom_id.id,
                        uom_id:line.uom_id.id,
                    }])
                }
            }
        );
 
        const bom_component = await this.pos.data.read("nf.bom.component",record.data.nf_bom_component_ids.resIds,["product_id", "product_qty", "bom_id", "uom_id", "nf_mrp_bom_id"]);
        bom_component[0].nf_mrp_bom_id.nf_bom_component_ids[0].bom_id.bom_line_ids.forEach((bom_line, index) => {
            const component = bom_component[index];

            if (component?.raw) {
                bom_line.product_qty = component.raw.product_qty;
            }
        });
        
        const mrp_bom = await bom_component[0].nf_mrp_bom_id;
        this.props.getPayload(mrp_bom);
        this.props.close();
    }

    closePopup(){
        this.props.close();
    }
}