import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";
import { patch } from "@web/core/utils/patch";

patch(OrderSummary.prototype, {
  _setValue(val) {
    super._setValue(val);
    if(this.pos.config.apply_commission){
      const newSelectedLine = this.currentOrder?.getSelectedOrderline();
  
      if (!newSelectedLine) {
        return;
      }
  
      const emp_id = newSelectedLine.nf_employee_id;
  
      if (emp_id && this.pos.config.apply_commission) {
        this.pos.nf_commission_calculation(
          newSelectedLine,
          emp_id
        );
      }
    }
  }
});

