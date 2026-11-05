import { Navbar } from "@point_of_sale/app/components/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { proxy, onWillStart, onMounted, signal } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import {
    makeAwaitable,
    ask,
    makeActionAwaitable,
} from "@point_of_sale/app/utils/make_awaitable_dialog";


patch(Navbar.prototype, {
    setup(){
        super.setup(...arguments);

        this.state = proxy({
            inputValue: '',
            partner : [],
            filteredPartners: [],
            currentFocus: -1,
        });
        this.action = useService("action");
        this.datalistRef = signal.ref();
        this.state.partner = [] //this.pos.models["res.partner"].getAll();
        this.state.filteredPartners = [] //this.state.partner;
        
        // onMounted(() => {
        //     // this.setupDropdownEvents();
        //     this.state.datalistRef = document.getElementById("nf-partnerContact");
        // });
    },

    searchButton(){
        const mobileImg = document.getElementById("nf_partner_mobile_search_icon").style.display = "none";
        const desktopSearch = document.getElementById("nf-contactInput")
        desktopSearch.style.display = "block";
        desktopSearch.focus();

            const hideinput = (event) => {
                if (!desktopSearch.contains(event.target)) {
                    desktopSearch.style.display = "none";
                    document.getElementById("nf_partner_mobile_search_icon").style.display = "block";

                    document.removeEventListener("click", hideinput);
                }
            };
            setTimeout(() => {
            document.addEventListener("click", hideinput);
        }, 0);
    },
    setupDropdownEvents() {
        const input = this.state.inputValue //this.inputRef.el;
        const datalist = document.getElementById("nf-partnerContact");
        console.log("datalist ????",datalist);
        
        
        
        if (!input || !datalist) return;
        
        if ( this.state.partner.length == 0 ){
            this.state.partner = this.pos.models["res.partner"].getAll();
            this.state.filteredPartners = this.state.partner;

        }

        const options = datalist.querySelectorAll('.nf_partner_option');    
        options.forEach(option => {
            option.onclick = () => {
                input.value = option.getAttribute('data-name') || option.value;
                datalist.style.display = 'none';
                input.style.borderRadius = "8px";
                

                const partner = this.state.partner.find(p => p.phone ? p.phone.replace(/\D/g, '').includes(option.value) : false);
                if (partner) {                    
                    this.pos.getOrder().setPartner(partner);
                    this.notification.add(_t("PoS Customer updated"), {
                        type: "warning",
                    });
                    setTimeout(() => {
                        input.value = '';
                        this.state.inputValue = '';
                    }, 1000);
                }
            };
        });
    },

    nfonClick(){
        let contact_length = this.pos.models["res.partner"].getAll();
        if ( contact_length.length != this.state.partner.length ){
            this.state.partner = contact_length
        }
    },
    nfonInputFocus(event) {
        // const datalist = this.datalistRef.el;
        const datalist = document.getElementById("nf-partnerContact");
        
        if (datalist) {
            datalist.style.display = 'block';
            event.target.style.borderRadius = "8px 8px 0 0";
        }
    },

    nfonInputBlur(event) {
        const datalist = document.getElementById("nf-partnerContact");
        setTimeout(() => {
            if (datalist) {
                datalist.style.display = 'none';
                event.target.style.borderRadius = "8px";
            }
        }, 200);
    },

    nfonInputChange(event) {
        const datalist = document.getElementById("nf-partnerContact");
        this.state.currentFocus = -1;
        const text = event.target.value.toUpperCase();
        this.state.inputValue = event.target.value;
        if (!datalist) return;

        const options = datalist.querySelectorAll('.nf_partner_option');
        
        if (text === '') {
            this.state.filteredPartners = this.state.partner;
            options.forEach(option => {
                option.style.display = "block";
            });
        } else {
            const filtered = [];
            options.forEach(option => {
                const name = option.getAttribute('data-name') || '';
                const phone = option.value || '';
                
                if (name.toUpperCase().indexOf(text) > -1 || phone.toUpperCase().indexOf(text) > -1) {
                    option.style.display = "block";
                    const partner = this.state.partner.find((p) => p.phone ? p.phone.replace(/\D/g, '').includes(phone) : false);
                    
                    if (partner) filtered.push(partner);
                } else {
                    option.style.display = "none";
                }
            });
            this.state.filteredPartners = filtered;
        }
    },
    getContactString(contact){
        if (contact){
            return contact.replace(/\D/g, '')
        }else{
            return ""
        }
    },
    async nfonKeyDown(event) {        
        event.stopPropagation();
        const partner_phone = event.target.value.toLowerCase();    
            
        const partnerlist = this.state.partner.filter(
        part =>
            part &&
            (
                (part.phone && part.phone.replace(/\D/g, '').includes(partner_phone)) ||
                (part.name && part.name.toLowerCase().includes(partner_phone))
            )
        );
        
        if (partnerlist.length <= 2){
            let domain = [['phone','ilike', partner_phone + "%"]]
            await this.pos.data.searchRead("res.partner", domain);
            this.state.partner = this.pos.models["res.partner"].getAll();
        }
        
        
        const datalist = document.getElementById("nf-partnerContact");
        if (!datalist) return;

        const options = Array.from(datalist.querySelectorAll('.nf_partner_option')).filter(
            opt => opt.style.display !== 'none'
        );

        // Arrow Down
        if (event.keyCode === 40) {
            event.preventDefault();
            this.state.currentFocus++;
            this.addActive(options);
        }
        // Arrow Up
        else if (event.keyCode === 38) {
            event.preventDefault();
            this.state.currentFocus--;
            this.addActive(options);
        }
        // Enter
        else if (event.keyCode === 13) {
            event.preventDefault();
            if (this.state.currentFocus > -1) {
                if (options[this.state.currentFocus]) {
                    options[this.state.currentFocus].click();
                }
            }
        }
        // Escape
        else if (event.keyCode === 27) {
            datalist.style.display = 'none';
            event.target.style.borderRadius = "8px";
            event.target.blur();
        }

        if(event.key === "Enter"){
            if(partnerlist.length === 0){
                const raw = event.target.value || "";
                const digits = raw.replace(/[^\d]/g, "");
                
                let additionalContext = {};
            
                if (/[a-zA-Z]/.test(raw)) {
                    // Letters exist → name
                    additionalContext = { default_name: raw };
                } else if (digits.length > 0) {
                    additionalContext = { 
                        default_phone: raw,   
                        default_name: false   
                    };
                }
                
                const record = await makeActionAwaitable(
                    this.action,
                    await this.pos.data.call("res.partner", "action_open_partner_view", [[]]),
                    {
                        additionalContext,
                    }
                );
                const newPartner = await this.pos.data.read("res.partner", record.config.resIds)                
                this.pos.getOrder().setPartner(newPartner[0]);
                this.state.inputValue = '';
                return newPartner[0];
            }
            else{
                this.pos.getOrder().setPartner(partnerlist[0]);
                this.notification.add(_t("PoS Customer updated"),{
                    type: "warning",
                });
                this.state.inputValue = '';
            }
        }
    },

    async createCustomer(raw){
        const input = document.querySelector("#nf-contactInput");
        if(raw){
            const digits = raw.replace(/[^\d]/g, "");
            let additionalContext = {};

            if (/[a-zA-Z]/.test(raw)) {
                additionalContext = { default_name: raw };
            } else if (digits.length > 0) {
                additionalContext = { 
                    default_phone: raw,   
                    default_name: false   
                };
            }
            
            const record = await makeActionAwaitable(
                this.action,
                await this.pos.data.call("res.partner", "action_open_partner_view", [[]]),
                {
                    additionalContext,
                }
            );
            const newPartner = await this.pos.data.read("res.partner", record.config.resIds)
            if(newPartner[0]){
                this.pos.getOrder().setPartner(newPartner[0]);
                this.notification.add(_t("PoS Customer updated"),{
                    type: "warning",
                });
                input.value = '';
                return newPartner[0];
            }
        }

    },

    addActive(options) {
        if (!options || options.length === 0) return;
        
        this.removeActive(options);
        
        if (this.state.currentFocus >= options.length) {
            this.state.currentFocus = 0;
        }
        if (this.state.currentFocus < 0) {
            this.state.currentFocus = options.length - 1;
        }
        
        options[this.state.currentFocus].classList.add("active");
        
        // Scroll into view
        options[this.state.currentFocus].scrollIntoView({
            block: 'nearest',
            behavior: 'smooth'
        });
    },

    removeActive(options) {
        options.forEach(option => {
            option.classList.remove("active");
        });
    },

    setInput(contact){
        const partner_phone = contact.target.value;
        const partner = this.state.partner.find(
            p => p.phone ? p.phone.replace(/\D/g, '').includes(partner_phone) : false
        );
        
        
        if(partner){
            this.pos.getOrder().setPartner(partner);
            this.state.inputValue = '';
            this.state.partner = this.pos.models["res.partner"].getAll();
            this.notification.add(_t("PoS Customer updated"),{
                type: "warning",
            });
        }
    },

});