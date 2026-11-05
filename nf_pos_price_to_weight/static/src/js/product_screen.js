import { patch } from "@web/core/utils/patch";
import { useBarcodeReader } from "@point_of_sale/app/hooks/barcode_reader_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        useBarcodeReader({
            price_to_weight: this._barcodePriceToWeight.bind(this)
        });
    },

     async _barcodePriceToWeight(code) {
        if (code.type !== "price_to_weight") {
            return super._barcodeProductAction(code);
        }
        
        const product = await this._getProductByBarcode(code);
        if (!product) { return false; }

        const vals = { product_id: product, product_tmpl_id: product.product_tmpl_id };
        const price = parseFloat(code.value) || 0;
        const productPrice = product[this.pos.config.nft_price_to_weight_selected];

        let quantity = 0;

        if (price !== 0 && productPrice !== 0) {
            quantity = price / productPrice;
        }
        vals.qty = quantity;
        
        await this.pos.addLineToCurrentOrder(
            vals,
            { code },
            product.needToConfigure()
        );
    },
})

// EAN-13 Barcode Rules:

// Example : Barcode =       0212345015502 (where first 12 are barcode digits and last is check digit)
// Barcode first 12 digits : 021234501550

// Calculation for check digit : 0×1 + 2×3 + 1×1 + 2×3 + 3×1 + 4×3 + 5×1 + 0×3 + 1×1 + 5×3 + 5×1 + 0×3 (digit1*1 + digi2*3 + digit3*1 ... digit12*3)
// Sum : 0 + 6 + 1 + 6 + 3 + 12 + 5 + 0 + 1 + 15 + 5 + 0 = 54
// 54 mod 10 = 4
// 10 - 4 = 6 (correct chck digit)
// Correct Barcode : 0212345015506
// False Barcode   : 0212345015502