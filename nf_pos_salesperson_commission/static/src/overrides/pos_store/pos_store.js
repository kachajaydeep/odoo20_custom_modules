import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {
  async nf_commission_calculation(selected_order_lines, employee) {
    let rules = this.models["pos.commission.rules"].filter(
      (rules) =>
        rules?.employee_ids.includes(employee) &&
        rules?.product_ids.includes(selected_order_lines.product_id)
    );

    let total_amount = 0;

    let new_pos_commission_line;
    let commission_amount = 0;

    if (rules.length !== 0) {
      const product_price = selected_order_lines.priceExcl;
      const product_qty = selected_order_lines.qty;

      for (let rule of rules) {
        let rule_line = selected_order_lines.pos_commission_line_ids.filter((x) => x.commission_rule_id.id == rule.id )
    
        if (rule_line.length && selected_order_lines.pos_commission_line_ids && selected_order_lines.pos_commission_line_ids.length){
            for (let i = 0; i < selected_order_lines.pos_commission_line_ids.length; i++) {
              const commission = selected_order_lines.pos_commission_line_ids[i];
              if ( commission.commission_rule_id.id == rule.id ){
                commission_amount = rule.amount;
                if (rule.commission_type === "percentage") {
                  total_amount = (product_price * commission_amount) / 100;
                } 
                else {
                  total_amount = commission_amount * product_qty;
                }                
                commission.update({commission_amount: total_amount})
                break;
              }
            }
        }
        else{
          commission_amount = rule.amount;  
          if (rule.commission_type === "percentage") {
            total_amount = (product_price * commission_amount) / 100;
          } 
          else {
            total_amount = commission_amount * product_qty;
          }
          
            new_pos_commission_line = await this.models[
              "pos.commission.line"
            ].create({
              commission_rule_id: rule,
              employee_id: employee,
              company_id:this.company,
              commission_amount: total_amount,
              product_id: selected_order_lines.product_id,
              order_line_id: selected_order_lines,
              state:'confirm'
            });
        }
        
      }

    }
    
    if(this.config.apply_commission){
      selected_order_lines.set_commission_employee(employee,total_amount);
    }
  },
});
