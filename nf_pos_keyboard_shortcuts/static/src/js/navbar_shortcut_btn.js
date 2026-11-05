import { Navbar } from "@point_of_sale/app/components/navbar/navbar";
import { ShortcutPopup } from "@nf_pos_keyboard_shortcuts/js/shortcut_popup";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(Navbar.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
    },

    openShortcutPopup() {
        this.dialog.add(ShortcutPopup, {});
    },
});