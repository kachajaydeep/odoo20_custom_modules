/** @odoo-module **/

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { ProductListView } from "@nf_pos_theme_app/js/overrides/productscreen/listComponent/productlist";
import { patch } from "@web/core/utils/patch";
import { proxy } from "@odoo/owl";


Object.assign(ProductScreen.components, { ProductListView });

patch(ProductScreen.prototype,{
    setup(){
        super.setup(...arguments)
        this.nf_state = proxy({
            nf_views : this.pos.config.nf_theme_setting_id?.product_view_selection || "grid"
        })
    },
    get nfproductViewMode() {
        const viewMode = this.productListView && this.ui.isSmall ? this.productListView : "grid";
        if (viewMode === "grid") {
            return "";
        } else {
            return "flex-row-reverse justify-content-between m-1";
        }
    },
    gridView(){
        this.nf_state.nf_views = "grid"
    },
    listView(){
        this.nf_state.nf_views = "list"
    }
})