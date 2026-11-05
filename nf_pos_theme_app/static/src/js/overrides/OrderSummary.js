// /** @odoo-module **/

// import { patch } from "@web/core/utils/patch";
// import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";

// patch(OrderSummary.prototype, {
//     clickLine(ev, orderline) {
//         super.clickLine(...arguments);
//         // posmodel.router?.state.current === "ProductScreen"

//         setTimeout(() => {
//             const padsElement = document.querySelector('.numpad');
        
//             if (padsElement && this.pos.router?.state.current === "ProductScreen") {
//                 if (padsElement.classList) {
//                     padsElement.classList.add('d-none');
//                     padsElement.classList.toggle('d-grid');
//                 }
//             }

//         }, 50);
//     },
// })