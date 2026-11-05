import { Component, proxy, onMounted, onWillStart, signal, App} from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { makeEnv, startServices } from "@web/env";
import { getTemplate } from "@web/core/templates";
import { registry } from "@web/core/registry";

class NfPriceCheckerKiosk extends Component {
    static template = "nf_price_checker_kiosk.NfPriceCheckerKiosk";
    setup(){
        this.state = proxy({
            product: null,
            barcode: "",
            settings: {},
            error: null,
            timer: null,
            theme:"dark"
        });

        this.inputRef = signal.ref();

        onWillStart(async () => {
            const nf_kiosk_setting = await rpc("/price_checker_kiosk/get_settings", {});
            this.state.settings = {
                show_name: nf_kiosk_setting.nf_show_name,
                show_image: nf_kiosk_setting.nf_show_image,
                show_code: nf_kiosk_setting.nf_show_code,
                show_barcode: nf_kiosk_setting.nf_show_barcode,
                show_price: nf_kiosk_setting.nf_show_price,
                show_stock: nf_kiosk_setting.nf_show_stock,
                show_specification: nf_kiosk_setting.nf_show_specification,
                show_category: nf_kiosk_setting.nf_show_category,
                show_keyboard: nf_kiosk_setting.nf_show_keyboard,
                show_product_weight:nf_kiosk_setting.nf_show_product_weight,
                show_product_sales_description:nf_kiosk_setting.nf_show_product_sales_description,
                show_product_tax:nf_kiosk_setting.nf_show_product_tax,
                logo: nf_kiosk_setting.company_logo,
                company_name: nf_kiosk_setting.company_name,
                company_config_logo:nf_kiosk_setting.company_config_logo ,
                company_config_name:nf_kiosk_setting.company_config_name ,
                show_pricelist: nf_kiosk_setting.nf_show_pricelist,
                pricelists: nf_kiosk_setting.nf_pricelists,
            };
        });

        onMounted(()=> {
            this.focusInput();
            document.addEventListener("click", () => this.focusInput());
        });
    }

    toggleTheme() {
        this.state.theme = this.state.theme === "dark" ? "light" : "dark";
        localStorage.setItem("nf_kiosk_theme", this.state.theme);
        this.applyTheme();
    }

    applyTheme() {
        if (this.state.theme === "light") {
            document.body.classList.add("light-mode");
        } else {
            document.body.classList.remove("light-mode");
        }
    }
    focusInput() {
        if (this.inputRef.el) {
            this.inputRef.el.focus();
        }
    }

    async onBarcodeEnter(ev) {
        if (ev.key === "Enter") {
            const barcode = this.state.barcode.trim();
            if (barcode) {
                await this.fetchProduct(barcode);
            }
        }
    }

    async fetchProduct(barcode) {
        this.state.error = null;
        try {
            const result = await rpc("/price_checker_kiosk/get_product_data", { barcode });
            
            if (result.error) {
                this.state.error = result.error;
                this.state.product = null;
            } else {
                this.state.product = result;
                this.resetTimer();
            }
        } catch (e) {
            this.state.error = "Connection error";
        }
        this.state.barcode = "";
    }

    resetTimer() {
        if (this.state.timer) {
            clearTimeout(this.state.timer);
        }
        // this.state.timer = setTimeout(() => {
        //     this.state.product = null;
        //     this.state.error = null;
        // }, 15000); // Clear after 10 seconds
    }

    onSearchClick() {
        const barcode = this.state.barcode.trim();
        if (barcode) {
            this.fetchProduct(barcode);
        }
    }

    onKeyClick(key) {
        if (key === "BACK") {
            this.state.barcode = this.state.barcode.slice(0, -1);
        } else if (key === "ENTER") {
            this.onSearchClick();
        } else if (key === "CLEAR") {
            this.state.barcode = "";
        } else {
            this.state.barcode += key;
        }
        this.focusInput();
    }

    get keys() {
        return ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "-", "Z", "X", "C", "V", "B", "N", "M", ".", "BACK", "ENTER"];
    }
    
}
registry.category("main_components").add("NfPriceCheckerKiosk", {
    Component: NfPriceCheckerKiosk,
});

// const mountKiosk = async () => {
//     const root = document.querySelector(".o_price_checker_kiosk");
//     if (!root) return;

//     // const env = await makeEnv();
//     // await startServices(env);

//     const app = new App(NfPriceCheckerKiosk, {
//         env,
//         getTemplate,
//         dev: env.debug ?? false,
//     });

//     await app.mount(root);
// };

// // Use native DOMContentLoaded or Odoo's whenReady if available
// if (document.readyState === "loading") {
//     document.addEventListener("DOMContentLoaded", mountKiosk);
// } else {
//     mountKiosk();
// }

export default NfPriceCheckerKiosk;