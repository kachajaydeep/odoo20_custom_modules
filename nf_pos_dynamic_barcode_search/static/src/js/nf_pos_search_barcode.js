odoo.define('require', function(require) {
    'use strict';

    var models = require('point_of_sale.models');
    var ProductScreen = require('point_of_sale.ProductScreen');
    var ProductsWidget = require('point_of_sale.ProductsWidget');
    const Registries = require('point_of_sale.Registries');
    const NumberBuffer = require('point_of_sale.NumberBuffer');


    const NfDynamicProductScreenInherit = (ProductScreen) =>
        class extends ProductScreen { 
            async _clickProduct(event) {
                var self = this;
                if (this.env.pos.config._nf_enable_dynamic_barcode_search && this.env.pos.dynamic_barcode_searched_code){
                    if (!this.currentOrder) {
                        this.env.pos.add_new_order();
                    }
                    const product = event.detail;
                    const options = await this._getAddProductOptions(product, this.env.pos.dynamic_barcode_searched_code);
                    if (!options) return;
                    if (self.env.pos.dynamic_barcode_searched_code.type === 'price') {
                        Object.assign(options, {
                            price: self.env.pos.dynamic_barcode_searched_code.value,
                            extras: {
                                price_manually_set: true,
                            },
                        });
                    } else if (self.env.pos.dynamic_barcode_searched_code.type === 'weight') {
                        Object.assign(options, {
                            quantity: self.env.pos.dynamic_barcode_searched_code.value,
                            merge: false,
                        });
                    } else if (self.env.pos.dynamic_barcode_searched_code.type === 'discount') {
                        Object.assign(options, {
                            discount: self.env.pos.dynamic_barcode_searched_code.value,
                            merge: false,
                        });
                    }
                    this.currentOrder.add_product(product, options);
                    NumberBuffer.reset();
                }else{
                    super._clickProduct(...arguments)
                }
            }
        }

    Registries.Component.extend(ProductScreen, NfDynamicProductScreenInherit);

    const NfDynamicProductsWidgetInherit = (ProductsWidget) =>
        class extends ProductsWidget {
            get productsToDisplay() {
                var self = this;
                var result = super.productsToDisplay;
                var list = [];
                this.env.pos.dynamic_barcode_searched_code = false
                if (this.searchWord !== '' && this.env.pos.config._nf_enable_dynamic_barcode_search) {
                    var dynamic_barcode_searched_code = this.env.pos.barcode_reader.barcode_parser.parse_barcode(this.searchWord)
                    if( dynamic_barcode_searched_code && dynamic_barcode_searched_code.value && dynamic_barcode_searched_code.value > 0 ){
                        list = this.env.pos.db.search_product_in_category(
                            this.selectedCategoryId,
                            dynamic_barcode_searched_code.base_code
                        );
                        if(list && list.length){
                            this.env.pos.dynamic_barcode_searched_code = dynamic_barcode_searched_code
                            result = list
                        }
                    }
                }
                return result
            }

        }

    Registries.Component.extend(ProductsWidget, NfDynamicProductsWidgetInherit);

    var Super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attributes,options){
            Super_order.initialize.apply(this, arguments);
            this.dynamic_barcode_searched_code = false
        },
    }) 

});