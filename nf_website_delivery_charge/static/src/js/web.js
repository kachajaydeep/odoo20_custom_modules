/** @odoo-module **/

import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export class NfWebsiteSaleDelivery extends Interaction {
    static selector = ".oe_website_sale";

    dynamicContent = {
        "#o_country_id": { "t-on-change": this.onChangeCountry },
    };

    async onChangeCountry() {
        const countryId = this.el.querySelector("#o_country_id").value;

        const result = await this.waitFor(
            rpc("/shop/nf_update_country", { country_id: countryId })
        );

        const citySelect = this.el.querySelector("#nf_city");
        citySelect.replaceChildren(); // native equivalent of $().empty()

        if (result) {
            for (const element of result) {
                const option = document.createElement("option");
                option.value = element.id;
                option.textContent = element.name;
                citySelect.appendChild(option);
            }
        }
    }
}

registry
    .category("public.interactions")
    .add("nf_website_sale_delivery.country_change", NfWebsiteSaleDelivery);