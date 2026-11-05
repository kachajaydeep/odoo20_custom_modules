import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
  get emp_name() {
        return this.nf_employee_id ? this.nf_employee_id.name : "";
  },
  set_commission_employee(emp,commission_price) {
    this.nf_employee_id = emp;
    this.commission_amount = commission_price;
  },
});
