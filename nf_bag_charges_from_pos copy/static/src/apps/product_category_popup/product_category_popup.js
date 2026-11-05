import { Component, proxy } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useService } from "@web/core/utils/hooks";


export class NfProductCategoryPopup extends Component {
    static template = "nf_bag_charges_from_pos.NfProductCategoryPopup";
    static components = { Dialog };
    static props = {
        templates: { type: Array },
        close: Function,
    };

    setup() {
        this.pos = usePos();
        this.state = proxy({
            quantities: {},
        });
    }

    getImageUrl(template) {
        return `/web/image/product.template/${template.id}/image_128`;
    }

    getQty(templateId) {
        return this.state.quantities[templateId] || 0;
    }

    get totalSelected() {
        return Object.values(this.state.quantities).reduce((a, b) => a + b, 0);
    }

    changeQty(templateId, delta) {
        const current = this.getQty(templateId);
        const next = Math.max(0, current + delta);
        this.state.quantities = {
            ...this.state.quantities,
            [templateId]: next,
        };
    }

    onClickProduct(template) {
        this.changeQty(template.id, 1);
    }

    async _fetchProduct(variantId) {
        const response = await fetch("/web/dataset/call_kw", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                jsonrpc: "2.0",
                method: "call",
                params: {
                    model: "product.product",
                    method: "read",
                    args: [[variantId], [
                        "id", "display_name", "lst_price",
                        "product_tmpl_id", "taxes_id",
                    ]],
                    kwargs: {},
                },
            }),
        });
        const json = await response.json();
        return json?.result?.[0] || null;
    }

    async onConfirm() {
        for (const [tmplIdStr, qty] of Object.entries(this.state.quantities)) {
            if (qty <= 0) continue;

            const tmplId = parseInt(tmplIdStr);
            const template = this.props.templates.find(t => t.id === tmplId);
            if (!template) continue;

            let product = this.pos.models["product.product"].find(
                p => p.id === template.variants[0].id
            );

            if (!product) {
                product = await this._fetchProduct(template.variants[0].id);
            }

            if (!product) continue;

            await this.pos.addLineToCurrentOrder(
                {
                    product_id: product,
                    price_unit: product.lst_price || template.list_price,
                    product_tmpl_id: product.product_tmpl_id,
                    qty: qty,
                },
                {}
            );
        }

        this.props.close();
    }

    onCancel() {
        this.props.close();
    }
}
