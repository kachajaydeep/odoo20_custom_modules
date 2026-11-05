import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, proxy } from "@odoo/owl";

export class ShortcutKeyField extends Component {
    static props = {
        ...standardFieldProps,
    };
    static template = "nf_pos_keyboard_shortcuts.ShortcutKeyField";
    setup() {
        this.state = proxy({ focused: false });
    }

    get value() {
        return this.props.record.data[this.props.name] || "";
    }

    onFocus() {
        this.state.focused = true;
    }

    onBlur() {
        this.state.focused = false;
    }

    onKeyDown(ev) {
        if (ev.key === "Tab") return;
        if (ev.key === "Escape") {
            ev.preventDefault();
            this.props.record.update({ [this.props.name]: "" });
            return;
        }
        if (ev.key === "Backspace") {
            ev.preventDefault();
            const current = this.value;
            if (!current) return;
            const parts = current.split("+");
            parts.pop();
            this.props.record.update({
                [this.props.name]: parts.join("+"),
            });
            return;
        }
        const modifierOnly = ["Control", "Shift", "Alt", "Meta"];
        if (modifierOnly.includes(ev.key)) return;

        ev.preventDefault();
        ev.stopPropagation();

        const keys = [];
        if (ev.ctrlKey) keys.push("CTRL");
        if (ev.shiftKey) keys.push("SHIFT");
        if (ev.altKey) keys.push("ALT");
        if (ev.metaKey) keys.push("META");

        keys.push(ev.key.toUpperCase());
        // keys.push(ev.key);

        this.props.record.update({
            [this.props.name]: keys.join(" + "),
        });
    }
}

registry.category("fields").add("shortcut_key", {
    component: ShortcutKeyField,
    supportedTypes: ["char"],
});