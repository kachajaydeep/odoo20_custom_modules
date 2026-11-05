import { ProductConfiguratorPopup } from "@point_of_sale/app/components/popups/product_configurator_popup/product_configurator_popup";
import { patch } from "@web/core/utils/patch";
import { proxy } from "@odoo/owl";


patch(ProductConfiguratorPopup.prototype, {
    setup() {
        super.setup();
        this.state = proxy({
            ...this.state,
            searchQuery:"",
        });
        this.pos.nfProductSearch = "";
    },

    get validAttributeLineIds() {
        const lines = super.validAttributeLineIds;
        const searchcategory = this.pos.nfProductSearch;
        if (!searchcategory) {
            return lines;
        }
        if (!this.pos.config.nf_enable_custom_variant){
            return lines
        }

        const searchableTerms = searchcategory
            .split(",")
            .map(term => term.trim().toLowerCase())
            .filter(term => term.length > 0);

        if (searchableTerms.length === 0) {
            return lines;
        }

        return lines.map((line, idx) => {
            const newLine = Object.create(line);

            newLine.values = () => {
                const currentTerm = lines.length === 1 ? searchableTerms[0] : searchableTerms[idx];

                if (!currentTerm) {
                    return line.values();
                }

                return line.values().filter(val => 
                    val.name.toLowerCase().includes(currentTerm)
                );
            };
            return newLine;
        });
    },

    nfProductCategory(ev){ 
        let value = ev?.target?.value || "";
        this.state.searchQuery = value;
        this.pos.nfProductSearch = value || "";
    },
    
    close(){
        this.props.close();
    }
})