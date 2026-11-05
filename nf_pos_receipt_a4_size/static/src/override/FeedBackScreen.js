import { FeedbackScreen } from "@point_of_sale/app/screens/feedback_screen/feedback_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { NfPrintPopup } from "@nf_pos_receipt_a4_size/apps/NfPrintPopup";

patch(FeedbackScreen.prototype, {
    setup(){
        super.setup();
        this.orm = useService("orm");
        this.report = useService("report");
    },
    async printA4Receipt() {
        // debugger;
        var self = this;        
        // this.dialog.add(NfPrintPopup, {
        //     order: this.currentOrder,
        // });
        const receipt = await this.orm.call("pos.order", "search_read", [[['pos_reference', '=', self.pos.getOrder().pos_reference]]]).then(function (callback) {
            self.report.doAction("nf_pos_receipt_a4_size.nf_a4_size_receipt_report_print", [
                callback[0].id,
            ]);
        });        
    }
})
