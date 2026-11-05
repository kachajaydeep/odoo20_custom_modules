import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

export class ProductPopUp extends Component {
    static template = "nf_pos_information.ProductPopUp";
    static components = {
        Dialog,
    };
    setup() {
        this.pos = usePos()
    }
    format_description() {
        if (this.props.product.description) {
            let row_data = (this.props.product.description)

            const tempDiv = document.createElement("div");
            tempDiv.innerHTML = row_data;

            const text = tempDiv.textContent || tempDiv.innerText || "";

            return text.trim()
        }
        else{
            return 'No description available'
        }
    }
}