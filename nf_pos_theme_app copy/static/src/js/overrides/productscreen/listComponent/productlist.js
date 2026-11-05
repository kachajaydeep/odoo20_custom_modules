/** @odoo-module **/

import { Component } from "@odoo/owl";

export class ProductListView extends Component {
    static template = "nf_pos_theme_app.ProductListView";
    
    static props = {
        onClick: { type: Function, optional:true },
        onProductInfoClick:{ type: Function, optional:true },
        class:{ type:String, optional:true },
        showWarning:{ type:Boolean, optional:true }
    }
}
