import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

export class ProductImagePopup extends Component{
    static template = 'nf_pos_image_preview.ImagePopup'
    static components = {
        Dialog,
    };
    setup(){
        this.pos = usePos()
    }
}