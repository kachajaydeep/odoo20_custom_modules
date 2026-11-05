import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { SelectionPopup } from "@point_of_sale/app/components/popups/selection_popup/selection_popup";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { useService } from "@web/core/utils/hooks";

patch(Orderline.prototype, {
    setup() {
        super.setup(...arguments);
        this.pos = usePos();
        this.dialog = useService('dialog');
    },

    async clickPricelist() {
        event?.stopPropagation();

        const pricelist = this.getPricelistList();
        const line = this.props.line;
        const product = line.product_id;

        const selectedPricelist = await makeAwaitable(this.dialog, SelectionPopup, {
            list: pricelist,
            title: _t("Pricelist Selection")
        });
        if (!selectedPricelist) return;

        line.setPricelist(selectedPricelist);

        if (product.type === 'combo') {
            const manualDiscount = line._manualDiscount ?? 0;
            line._applyingPricelist = false;
            line.setDiscount(manualDiscount);
            return;
        }

        const qty = this.getQuantity();

        let final_price = 0;
        let extraPrice = 0;
        const attrs = line?.attribute_value_ids;
        if (attrs && Array.isArray(attrs)) {
            extraPrice = attrs.reduce((sum, attr) => sum + (attr?.price_extra || 0), 0);
        }

        if (extraPrice !== 0) {
            const basePrice = product.product_tmpl_id?.list_price || 0;
            const discountedBase = product.getPrice(selectedPricelist, qty, false, false);
            const discountRatio = basePrice > 0 ? (discountedBase / basePrice) : 1;
            final_price = (basePrice + extraPrice) * discountRatio;
        } else {
            final_price = product.getPrice(selectedPricelist, qty, 0, false);
        }

        line.setUnitPrice(final_price);
    },

    getPricelistList() {
        const selectionList = this.pos.config.availablePricelists.map((pricelist) => ({
            id: pricelist.id,
            label: pricelist.name,
            isSelected:
                this.props.line.pricelist_id &&
                pricelist.id === this.props.line.pricelist_id.id,
            item: pricelist,
        }));

        if (!this.pos.config.pricelist_id) {
            selectionList.push({
                id: null,
                label: _t("Default Price"),
                isSelected: !this.props.line.pricelist_id,
                item: null,
            });
        }
        return selectionList;
    },

    getQuantity() {
        return this.props.line.qty;
    },
});
