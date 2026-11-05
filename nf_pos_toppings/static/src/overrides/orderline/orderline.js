import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

patch(Orderline, {
  props: {
    ...Orderline.props,
    line: {
      ...Orderline.props.line,
      shape: {
        ...Orderline.props.line.shape,
        nf_child_orderline_id: { type: String, optional: true },
      },
    },
  },
});