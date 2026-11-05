import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { PosSalesPerson } from "@nf_pos_salesperson_commission/app/popup/pos_saleperson_popup";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

patch(ControlButtons.prototype,{
    async salesPerson() {
        const payload = await makeAwaitable(
          this.dialog,
          PosSalesPerson,
          {}
        );
    },
});
