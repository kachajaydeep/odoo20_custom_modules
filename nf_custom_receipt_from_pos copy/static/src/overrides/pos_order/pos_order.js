/** @odoo-module **/
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";
import { GeneratePrinterData } from "@point_of_sale/app/utils/printer/generate_printer_data";

patch(PosOrder.prototype, {
    getNfReceiptTemplate(){
        const templateValue = this.config?.nf_receipt_template_id;
        if(!templateValue){
            return null;
        }
        const templates = this.model.models["nf.receipt.template"];        
        if(!templates){
            return null;
        }
        return templates.find((template) => template.id === templateValue.id)
    }
})