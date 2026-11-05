import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";


export class PosSalesPerson extends Component {
  static template = "nf_pos_salesperson_commission.PosSalesPerson";
  static components = { Dialog };

  setup() {
    this.pos = usePos();
    this.dialog = useService("dialog");

    this.state = useState({
      commission_ids: this.pos.config.commission_employee_ids || [],
    });
  }

  async getSalesPerson(employee){    
      if(employee && this.pos.config.apply_commission){
           let selected_line = await this.pos.getOrder().getSelectedOrderline()
           if(this.pos.config.apply_commission){
             await this.pos.nf_commission_calculation(selected_line,employee)   
           }
      }

    this.props.close()
  }

  confirm() {
    this.props.close();
  }
  close() {
      this.props.close();
  }
}

