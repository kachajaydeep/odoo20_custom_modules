import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

patch(Orderline, {
  props: {
    ...Orderline.props,
    line: {
      ...Orderline.props.line,
    },
  },
});

patch(Orderline.prototype, {
  setup() {
    this.pos = usePos();
  },
  async deleteItem() {
    const order = this.pos.getOrder();
    let selectedLine = this.pos.getOrder().getSelectedOrderline();

    await order.removeOrderline(selectedLine);
  },
});