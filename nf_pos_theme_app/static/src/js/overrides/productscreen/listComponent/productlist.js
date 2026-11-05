/** @odoo-module **/

import { Component } from "@odoo/owl";

export class ProductListView extends Component {
    static template = "nf_pos_theme_app.ProductListView";

    static defaultProps = {
        onClick: () => {},
        onProductInfoClick: () => {},
        class: "",
        showWarning: false,
    };
}
