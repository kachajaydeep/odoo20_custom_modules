/** @odoo-module **/

import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";
import { patch } from "@web/core/utils/patch";

patch(ActionpadWidget.prototype ,{
    nfCreateNewOrder(){
        // const button = document.querySelector('.list-plus-btn');
        const uploadicon = document.getElementsByClassName("fa-upload")[0];
        const pendingOrderbtn = uploadicon.parentElement;
        pendingOrderbtn.click();
        // button.click();
    }
})