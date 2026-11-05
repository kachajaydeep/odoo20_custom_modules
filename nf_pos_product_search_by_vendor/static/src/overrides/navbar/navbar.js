import { Navbar } from "@point_of_sale/app/components/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { proxy } from "@odoo/owl";

patch(Navbar.prototype, {
    setup() {
        super.setup(...arguments);
        this.state = proxy({
            searchProductByVendor:"",
        })
        this.pos.nfProductToSearchVendor = "";
    },
    
    nfSearchProductByVendor(ev){
        let value = ev?.target?.value || "";
        this.state.searchProductByVendor = value;
        this.pos.nfProductToSearchVendor = value;
        
    },

    searchButton(){
        const desktopSearch = document.getElementById("nf-vendor")
        const displayValue = window.getComputedStyle(desktopSearch).display;
 
        if(displayValue == "none"){
            desktopSearch.style.display = "block";
        }
        else{
            desktopSearch.style.display = "none";
        }
        
    }
})