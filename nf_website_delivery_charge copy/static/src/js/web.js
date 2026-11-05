/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export class NFWebsiteSaleDelivery extends Component {
    static template = "nf_website_delivery_charge.NFWebsiteSaleDelivery";
    static props = {};

    setup() {
        // Nothing needed here for now.
    }

    async onChangeCountry(ev) {
        const countryId = ev.target.value;
        const citySelect = document.querySelector("#nf_city");

        if (!citySelect) {
            return;
        }

        citySelect.innerHTML = "";

        if (!countryId) {
            return;
        }

        try {
            const result = await rpc("/shop/nf_update_country", {
                country_id: parseInt(countryId),
            });

            if (result && result.length) {
                for (const city of result) {
                    const option = document.createElement("option");
                    option.value = city.id;
                    option.textContent = city.name;
                    citySelect.appendChild(option);
                }
            }
        } catch (error) {
            console.error("Error loading cities:", error);
        }
    }
}

registry
    .category("public_components")
    .add("nf_website_delivery_charge.NFWebsiteSaleDelivery", NFWebsiteSaleDelivery);
