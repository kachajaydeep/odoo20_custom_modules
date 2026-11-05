/** @odoo-module **/

import { Component, proxy, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";

export class AddSectionDeleteDialog extends Component {

    static template = "nf_action_delete_view";

    static components = {
        Dialog,
    };

    static props = {
        close: Function,
        lineId: Number,
        recordId: { type: Number, optional: true },
        model: String,
    };

    setup() {

        this.orm = useService("orm");
        this.action = useService("action");

        this.state =proxy({
            lineCount: 0,
        });

        onWillStart(async () => {
            this.state.lineCount = await this.getLineCount();
        });
    }

    close() {
        this.props.close();
    }

    async _getLines() {

        const fieldsToRead = [];

        if (
            this.props.model === "sale.order.line" ||
            this.props.model === "purchase.order.line"
        ) {
            fieldsToRead.push("order_id");
        }

        if (this.props.model === "account.move.line") {
            fieldsToRead.push("move_id");
        }

        const currentLine = await this.orm.read(
            this.props.model,
            [this.props.lineId],
            fieldsToRead
        );

        let domain = [];

        if (
            this.props.model === "sale.order.line" ||
            this.props.model === "purchase.order.line"
        ) {
            domain = [
                ["order_id", "=", currentLine[0].order_id[0]]
            ];
        } else {
            domain = [
                ["move_id", "=", currentLine[0].move_id[0]]
            ];
        }

        return await this.orm.searchRead(
            this.props.model,
            domain,
            [
                "id",
                "name",
                "display_type",
                "sequence",
                "nf_section_name",
            ],
            {
                order: "sequence,id",
            }
        );
    }

    async getLineCount() {

        const lines = await this._getLines();

        const currentSection = lines.find(
            line =>
                line.id === this.props.lineId &&
                line.display_type === "line_section"
        );

        if (!currentSection) {
            return 0;
        }

        let count = 0;

        for (const line of lines) {

            // Skip sections
            if (line.display_type === "line_section") {
                continue;
            }

            // Skip invoice payment terms
            if (
                this.props.model === "account.move.line" &&
                line.display_type === "payment_term"
            ) {
                continue;
            }

            if (line.nf_section_name === currentSection.name) {
                count++;
            }
        }

        return count;
    }

    async deleteOnlySection() {        
        const lines = await this._getLines();

        const selectedSection = lines.find(
            line =>
                line.id === this.props.lineId &&
                line.display_type === "line_section"
        );

        if (!selectedSection) {
            return;
        }

        const sectionIds = lines
            .filter(
                line =>
                    line.display_type === "line_section" &&
                    line.name === selectedSection.name
            )
            .map(line => line.id);

        if (sectionIds.length) {
            await this.orm.unlink(
                this.props.model,
                sectionIds
            );
        }

        this.close();

        this.action.doAction({
            type: "ir.actions.client",
            tag: "reload",
        });
    }

    async deleteSectionWithLines() {

        const lines = await this._getLines();

        const selectedSection = lines.find(
            line =>
                line.id === this.props.lineId &&
                line.display_type === "line_section"
        );

        if (!selectedSection) {
            return;
        }

        const idsToDelete = [];

        for (const line of lines) {

            // Delete all sections with same name
            if (
                line.display_type === "line_section" &&
                line.name === selectedSection.name
            ) {
                idsToDelete.push(line.id);
                continue;
            }

            // Skip payment terms on invoices/bills
            if (line.display_type === "payment_term") {
                continue;
            }

            // Delete products belonging to same section
            if (line.nf_section_name === selectedSection.name) {
                idsToDelete.push(line.id);
            }
        }
        
        if (idsToDelete.length) {
            await this.orm.unlink(
                this.props.model,
                [...new Set(idsToDelete)]
            );
        }

        this.close();

        this.action.doAction({
            type: "ir.actions.client",
            tag: "reload",
        });
    }
}