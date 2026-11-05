/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { actionService } from "@web/webclient/actions/action_service";
import { registry } from "@web/core/registry";
import { rpc, rpcBus } from "@web/core/network/rpc";

registry.category("ir.actions.report handlers").add("nf_print_pdf_report", async (action, options, env) => {
    const companyId = action.context?.allowed_company_ids?.[0];
    
    const ids = action.context?.active_ids ||
    (action.context?.active_id ? [action.context.active_id] : []);

    const dataPayload = action.data || null;

    try {
        const [company] = await rpc("/web/dataset/call_kw", {
            model: "res.company",
            method: "read",
            args: [[companyId], ["nf_automatically_print_pdf_report"]],
            kwargs: {},
        });
        
        const autoPrint = company?.nf_automatically_print_pdf_report;

        if (!autoPrint) {
            return;
        }

        const data = await rpc("/web/nfprintpdf", {
            report_name: action.report_name,
            res_ids: ids,
            data: dataPayload,   // 🔥 important
        });

        if (data) {
            printJS({
                printable: data,
                type: "pdf",
                base64: true
            });
        }

    } catch (error) {
        console.error("RPC Error:", error);
    }
}, { sequence: 1 }); // Sequence 1 ensures this runs BEFORE the default Odoo handlers