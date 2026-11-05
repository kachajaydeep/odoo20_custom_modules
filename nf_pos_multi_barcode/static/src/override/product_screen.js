/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { useBarcodeReader } from "@point_of_sale/app/hooks/barcode_reader_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        this.notification = useService("notification");
        useBarcodeReader({
            multi_barcode: this._multiBarcodeAction.bind(this),
        });
    },
    async _getProductByMultiBarcode(code) {
        let product = this.pos.models["product.product"].find((p) =>
            (p.barcode_ids || []).some((b) => b.name === code.base_code)
        );
        
        if (!product) {
            const template = this.pos.models["product.template"].find((p) =>
                (p.barcode_ids || []).some((b) => b.name === code.base_code)
            );
    
            if (template) {
                product = this.pos.models["product.product"].find(
                    (p) => p.product_tmpl_id?.id === template.id
                );
            }
        }

        return product || false;
    },

    async _multiBarcodeAction(code) {
        if (!this.pos.config.nf_enable_pos_multi_barcode) {
            this.notification.add(
                _t(
                    "The Point of Sale could not find any product, customer, employee or action associated with the scanned barcode."
                ),
                {
                    type: "warning",
                    title: _t(`Unknown Barcode`) + " " + (code.code),
                }
            );
            this.sound.play("error");
            return;
        }
        const product = await this._getProductByMultiBarcode(code);

        if (!product) {
            this.notification.add(_t("No Product Found with the given Barcode!"), { type: "warning" });
            return;
        }

        await this.pos.addLineToCurrentOrder(
            {
                product_id: product,
                product_tmpl_id: product.product_tmpl_id
            },
            { code },
            product.needToConfigure()
        );
        this.numberBuffer.reset();
    }
})