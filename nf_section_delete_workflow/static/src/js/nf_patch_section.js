/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { SectionAndNoteListRenderer } from "@account/components/section_and_note_fields_backend/section_and_note_fields_backend";
import { AddSectionDeleteDialog } from "./nf_add_section_delete_dialog";

patch(SectionAndNoteListRenderer.prototype, {

    setup() {
        super.setup(...arguments);
        this.dialog = useService("dialog");
    },

    async deleteSection(record, ev) {

        const model = record.resModel || "";

        // Only handle supported models
        const supportedModels = [
            "account.move.line",
            "sale.order.line",
            "purchase.order.line",
        ];

        // Important : let Odoo handle everything else safely
        if (!supportedModels.includes(model)) {
            return super.deleteSection(record, ev);
        }

        const lineId = record.resId;

        if (!lineId) {
                return super.deleteSection(record, ev);
            }

        const moveId =
            record.data?.move_id?.[0] ||
            record.data?.order_id?.[0] ||
            this.props?.list?.record?.resId ||
            this.props?.list?.model?.root?.resId ||
            null;

        this.dialog.add(AddSectionDeleteDialog, {
            lineId,
            recordId: moveId,
            model,
        });
    },
});