import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SelectionPopup } from "@point_of_sale/app/components/popups/selection_popup/selection_popup";

patch(ControlButtons.prototype, {
    async selectUom(){
        const selectedOrderline = this.currentOrder?.getSelectedOrderline();
        const product = selectedOrderline?.product_id;
        
        if (!product) return;

        const uomList = this.getAvailableUom(product, selectedOrderline);

        const uom_selected = await makeAwaitable(this.dialog, SelectionPopup, {
            list: uomList,
            title: _t("UOM Selection")
        });

        if (!uom_selected){
            selectedOrderline.selected_uom_id = product.uom_id;
            selectedOrderline.setQuantity(1);
            selectedOrderline.setUnitPrice(product.lst_price);
            selectedOrderline.price_type = 'original';
            return;
        }

        try {
            const orm = this.env.services.orm;
            const updated_price = await orm.call(
                "product.template",
                "get_price_for_uom",
                [product.product_tmpl_id.id, uom_selected.id],
            );

            selectedOrderline.setQuantity(1);
            selectedOrderline.setUnitPrice(updated_price);
            selectedOrderline.price_type = 'manual';

            selectedOrderline.selected_uom_id = uom_selected;
        }
        catch (e){
            console.error("RPC ERROR", e);
        }
    },
    getAvailableUom(product, selectedOrderline) {
        const tmpl = product.product_tmpl_id;
        const currentUomId = selectedOrderline?.selected_uom_id?.id || product.uom_id?.id;

        const uomList = tmpl.uom_ids.map((uom) => ({
            id: uom.id,
            label: uom.name,
            isSelected: uom.id === currentUomId,
            item: uom,
        }));

        if (!uomList.length) {
            const uom = product.uom_id;
            uomList.push({
                id: uom.id,
                label: uom.name,
                isSelected: true,
                item: uom,
            });
        }
        return uomList;
    },
});