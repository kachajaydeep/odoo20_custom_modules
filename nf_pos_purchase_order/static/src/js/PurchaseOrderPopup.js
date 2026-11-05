/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { Component, markup, useProps } from "@odoo/owl";
import { ask } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

export class PurchaseOrderPopup extends Component {
    static template = "nf_pos_purchase_order.PurchaseOrderPopup"
    static components = { Dialog };
    static props = [
        "close",
        "vendor_id?",
        "order",
        "po_status",
        "validate_po_receipt",
        "create_bill",
    ];

    props = {
        confirmText: _t("Create"),
        cancelText: _t("Close"),
        title: _t("Create RFQ / Purchase Order"),
    };

    setup() {
        super.setup(...arguments);
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.currentOrder = this.pos.getOrder();
        this.orm = useService("orm");
        this.report = useService("report");
        this.notification = useService("notification");
        this.partners = this.pos.models["res.partner"].getAll();
        this.changes = {
            partners: this.partners,
            vendor_id: this.currentOrder.getPartner()?.id || this.partners[0]?.id || false,
            po_status: this.pos.config.po_status,
            validate_po_receipt: this.pos.config.validate_po_receipt,
            create_bill: this.pos.config.create_bill,
        }        
        this.numberBuffer = useService("number_buffer");
        this.numberBuffer.use({
            triggerAtEnter: () => this.OnConfirmCreatePO(),
            triggerAtEscape: () => this.cancel(),
            state: this.changes,
        });
    }

    OnChange(event) {        
        if (event.target.type == 'checkbox') {
            this.changes[event.target.name] = event.target.checked;
        } else {
            this.changes[event.target.name] = event.target.value;
        }
        if (event.target.name !== 'vendor_id') {
            this.verifyChanges(event)
        }
    }

    verifyChanges(event) {
        let changes = this.changes;
        if (changes.validate_po_receipt && changes.po_status !== 'purchase') {
            return this.dialog.add(ConfirmationDialog, {
                title: _t('Error'),
                body: _t('Please select auto confirm to be able to auto receipt'),
            })
        }
        if (changes.create_bill && (po_status !== 'purchase' || !changes.validate_po_receipt)) {
            return this.dialog.add(ConfirmationDialog, {
                title: _t('Error'),
                body: _t('Please select auto confirm and auto receipt to be able to auto bill'),
            })
        }
    }

    async OnConfirmCreatePO() {
        let order = this.currentOrder;
        var employee_id = false;
        if (this.pos.config.module_pos_hr) {
            employee_id = this.pos.getCashier().id
        }
        let value = {
            origin: "POS: " + this.pos.config.name,
            partner_id: this.changes.vendor_id,
            pos_session_id: this.pos.session.id,
            employee_id: employee_id,
            order_line: [],
        }
        
        for (var i = 0; i < order.lines.length; i++) {
            var line = order.lines[i];
            var line_val = order._convert_pos_line_to_po_line(line);
            value.order_line.push(line_val);
        }
        
        let result = await this.orm.call(
            "purchase.order",
            "create_from_pos_ui",
            [
                value,
                this.changes.po_status,
                this.changes.validate_po_receipt,
                this.changes.create_bill,
            ]
        )

        this.pos.removeOrder(this.currentOrder);
        this.pos.selectNextOrder();
        this.env.dialogData.close()

        this.notification.add(
            _t("Purchase Order %(name)s has been created successfully!", { name: result.name }),
            { type: "success" },
            3000
        );
        const confirmed = await ask(this.dialog, {
            body: markup(
                _t(
                    `Print Purchase Order <style>.po-print-link { color: #1a73e8 !important; text-decoration: underline;} .po-print-link:hover {color: #0b47a1;text-decoration: underline;}</style><a class='po-print-link' href='/odoo/purchase/%(id)s?model=purchase.order' target='_blank'>%(name)s</a> ?`,
                    { id: result.id, name: result.name }
                )
            ),
            confirmLabel: _t("Print"),
            cancelLabel: _t("Cancel"),
        });
        if (confirmed) {
            return await this.report.doAction("purchase.action_report_purchase_order", [result.id]);
        }
        else {
            return false;
        }
    }
}