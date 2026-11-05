import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";

patch(PosStore.prototype, {
    logOutUser() {
        browser.navigator.serviceWorker?.controller?.postMessage("user_logout");
        browser.location.replace("/web/session/logout");
    }
})