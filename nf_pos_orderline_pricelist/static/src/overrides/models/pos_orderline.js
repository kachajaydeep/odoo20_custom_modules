import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { formatCurrency } from "@web/core/currency";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {

    setPricelist(pricelist) {
        this.nf_line_total = formatCurrency(this.getbasePrice(),this.currency.id);
        this.pricelist_id = pricelist || false;
    },

    getPricelist() {
        return this.pricelist_id;
    },

    setDiscount(discount) {
        super.setDiscount(discount);
        const pricelist = this.pricelist_id;
        if (!pricelist || this._applyingPricelist) return;
        this._manualDiscount = discount;
        this._originalFixedDiscount = discount;
        if (this.product_id?.type === 'combo') {
            this._applyPricelistToCombo(this, this.product_id, pricelist);
        }
    },

    setUnitPrice(price) {
        if (!this.pricelist_id || this.price_type === 'manual') {
            this.pricelist_id = this.config?.pricelist_id;
        }
        super.setUnitPrice(price);
    },

    setQuantity(quantity, keep_price) {
        const result = super.setQuantity(...arguments);
        const pricelist = this.pricelist_id;
        const product = this.product_id;

        if (this.price_type === 'manual' || !pricelist) return result;

        if (product?.type === 'combo') {
            this._applyPricelistToCombo(this, product, pricelist);
            return result;
        }

        let extraPrice = 0;
        const attrs = this.attribute_value_ids;
        if (Array.isArray(attrs)) {
            extraPrice = attrs.reduce((sum, attr) => sum + (attr?.price_extra || 0), 0);
        }

        const unit_price = extraPrice
            ? (() => {
                const basePrice = product.product_tmpl_id?.list_price || 0;
                const discountedBase = product.getPrice(pricelist, quantity, false, false);
                const ratio = basePrice > 0 ? discountedBase / basePrice : 1;
                return (basePrice + extraPrice) * ratio;
            })()
            : product.getPrice(pricelist, quantity, 0, false, product);

        this.setPricelist(pricelist);
        this.setUnitPrice(unit_price);
        return result;
    },

    getbasePrice() {
        const unit_price = this._getUnitPrice(
            this.config.pricelist_id,
            this.qty,
            this.price_extra,
            this.product_id
        );
        return this._applyTax(unit_price, this.tax_ids?.[0], this.qty);
    },

    // Unified tax application for single tax
    _applyTax(unit_price, tax, quantity = 1) {
        if (!tax?.amount_type) return unit_price * quantity;

        const amt = tax.amount;
        switch (tax.amount_type) {
            case 'percent': return (unit_price + unit_price * amt / 100) * quantity;
            case 'fixed': return (unit_price + amt) * quantity;
            case 'division': return (unit_price / (1 - amt / 100)) * quantity;
            case 'group': {
                const extra = (tax.children_tax_ids || []).reduce((sum, child) => {
                    if (child.amount_type === 'percent')
                        return sum + unit_price * child.amount / 100;
                    if (child.amount_type === 'division')
                        return sum + (unit_price / (1 - child.amount / 100)) - unit_price;
                    return sum + child.amount;
                }, 0);
                return (unit_price + extra) * quantity;
            }
            default: return unit_price * quantity;
        }
    },

    // Compute tax amount only (no quantity, no base)
    _taxAmount(unitPrice, tax) {
        if (!tax?.amount_type) return 0;
        const amt = tax.amount;
        switch (tax.amount_type) {
            case 'percent':
                return tax.price_include
                    ? unitPrice - unitPrice / (1 + amt / 100)
                    : unitPrice * amt / 100;
            case 'fixed': return amt;
            case 'division': return unitPrice / (1 - amt / 100) - unitPrice;
            case 'group':
                return (tax.children_tax_ids || []).reduce((sum, child) => {
                    if (child.amount_type === 'percent')
                        return sum + (child.price_include
                            ? unitPrice - unitPrice / (1 + child.amount / 100)
                            : unitPrice * child.amount / 100);
                    if (child.amount_type === 'division')
                        return sum + unitPrice / (1 - child.amount / 100) - unitPrice;
                    return sum + child.amount;
                }, 0);
            default: return 0;
        }
    },

    _getComboTotalWithTax(line, price) {
        const parentTaxIds = line.tax_ids || line.product_id?.taxes_id || [];

        // Tax on parent
        if (parentTaxIds.length > 0) {
            return price + parentTaxIds.reduce(
                (sum, tax) => sum + this._taxAmount(price, tax), 0
            );
        }

        // Tax on children
        const comboLines = [...line.combo_line_ids];
        if (comboLines.length > 0) {
            const fullChildTotal = comboLines.reduce((s, cl) => s + (cl.price_unit || 0), 0);
            const ratio = fullChildTotal > 0 ? price / fullChildTotal : 1;
            return comboLines.reduce((sum, cl) => {
                const childPrice = (cl.price_unit || 0) * ratio;
                const childTaxIds = cl.tax_ids || cl.product_id?.taxes_id || [];
                const childTax = childTaxIds.reduce(
                    (s, tax) => s + this._taxAmount(childPrice, tax), 0
                );
                return sum + childPrice + childTax;
            }, 0);
        }

        return price;
    },

    _getUnitPrice(pricelist, qty, extraPrice, product) {
        return product.getPrice(pricelist, qty, extraPrice, false, product);
    },

    _applyPricelistToCombo(line, product, selectedPricelist) {
        if (!selectedPricelist || !product?.lst_price) return;

        try {
            line._applyingPricelist = true;

            const lstPrice = product.lst_price;
            const fixedDiscount = line._manualDiscount ?? 0;
            const pricelistPrice = product.getPrice(selectedPricelist, 1, false, false);

            const pricelistRatio = lstPrice > 0
                ? Math.round((pricelistPrice / lstPrice) * 1e10) / 1e10
                : 1;
            const fixedRatio = 1 - fixedDiscount / 100;

            const combinedDiscountPercent = Math.round(
                (1 - pricelistRatio * fixedRatio) * 10000
            ) / 100;

            const comboExtraPrice = [...line.combo_line_ids].reduce((sum, cl) => {
                const attrs = cl.attribute_value_ids;
                return sum + (Array.isArray(attrs)
                    ? attrs.reduce((s, a) => s + (a?.price_extra || 0), 0)
                    : 0);
            }, 0);

            const fullSalePrice = lstPrice + comboExtraPrice;
            const discountedPrice = fullSalePrice * pricelistRatio * fixedRatio;

            line._originalComboPrice = line._getComboTotalWithTax(line, fullSalePrice);
            line._discountedComboPrice = line._getComboTotalWithTax(line, discountedPrice);
            line.discount = combinedDiscountPercent;

            for (const childLine of line.combo_line_ids) {
                childLine._applyingPricelist = true;
                childLine.discount = combinedDiscountPercent;
                childLine._applyingPricelist = false;
            }

        } catch (e) {
            console.error("Combo pricelist error:", e);
        } finally {
            line._applyingPricelist = false;
        }
    },

    get price() {
        return (this.product_id?.type === 'combo' && this._discountedComboPrice)
            ? this._discountedComboPrice
            : super.price;
    },

    get displayPrice() {
        return (this.product_id?.type === 'combo' && this._discountedComboPrice)
            ? this._discountedComboPrice
            : super.displayPrice;
    },

    // Keep for backward compat — now delegates to _applyTax
    getFinalAmountWithTax(taxes, taxType, unit_price, quantity) {
        return this._applyTax(unit_price, taxes, quantity);
    },
});