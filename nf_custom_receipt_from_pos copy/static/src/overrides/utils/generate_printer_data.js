// import { patch } from "@web/core/utils/patch";
// import { GeneratePrinterData } from "@point_of_sale/app/utils/printer/generate_printer_data";

// patch(GeneratePrinterData.prototype, {
//   generateReceiptData() {
//     const data = super.generateReceiptData(...arguments);

//     const config = this.config;
//     const template = config.nf_receipt_template_id;

//     data.extra_data = {
//       ...data.extra_data,

//       nf_custom_receipt_template_enabled: !!config.nf_custom_receipt_template,

//       nf_custom_receipt_template_name: template
//         ? `nf_custom_receipt_from_pos.Receipt${template.id}`
//         : false,
//     };

//     const temp = this.order.getNfReceiptTemplate();
//     // data.order.nf_receipt_template = temp ? temp.nf_receipt_xml : null;
//     // console.log("data here ???????",data.order);

//     data.nf_receipt_template = temp ? temp.nf_receipt_xml : null;

//     const xml = data.nf_receipt_template;

//         if (xml) {
//             const body = xml
//                 .replace(/^\s*<t\b[^>]*>/i, "")
//                 .replace(/<\/t>\s*$/i, "")
//                 .trim();

//             const parser = new DOMParser();
//             const doc = parser.parseFromString(body, "text/xml");

//             const parserError = doc.querySelector("parsererror");

//             if (!parserError) {
//                 data.nf_html_data = new XMLSerializer().serializeToString(doc);
//             } else {
//                 console.error("Invalid receipt XML:", parserError.textContent);
//                 data.nf_html_data = null;
//             }
//         } else {
//             data.nf_html_data = null;
//         }

//     return data
//   },

//   // const body = xml
//   // .replace(/^\s*<t\b[^>]*>/i, "")
//   // .replace(/<\/t>\s*$/i, "")
//   // .trim();

//   // const parser = new DOMParser();

//   // const doc = parser.parseFromString(
//   //     body,
//   //     "text/xml"
//   // );
//   // data.nf_html_data = doc
//   // console.log("doc here ???",data);
//   // return data;

//   // renderCustomReceipt() {
//   //     const xml = this.generateReceiptData().nf_receipt_template;
//   //     console.log("xml ???",xml);

//   //     if(!xml){
//   //         return
//   //     }
//   //     const body = xml
//   //     .replace(/^\s*<t\b[^>]*>/i, "")
//   //     .replace(/<\/t>\s*$/i, "")
//   //     .trim();

//   //     console.log("body ????",body);

//   //     const parser = new DOMParser();

//   //     const doc = parser.parseFromString(
//   //         data.nf_receipt_template,
//   //         "text/xml"
//   //     );

//   //     console.log(doc);
//   // }

//   // generateReceiptData() {
//   //     const data = super.generateReceiptData(...arguments);
//   //     const config = this.config;
//   //     const template = config.nf_custom_receipt_template && config.nf_receipt_template_id;
//   //     data.extra_data = data.extra_data || {};

//   //     data.extra_data.nf_custom_receipt_template_name = template
//   //         ? `nf_pos_custom_receipt.nf_receipt_design_template_${template.id}`
//   //         : false;
//   //     return data;
//   // },

//   //   generateReceiptData() {
//   //         const data = super.generateReceiptData(...arguments);

//   //         const config = this.config;

//   //         console.log("NF CONFIG:", config);
//   //         console.log(
//   //             "NF TEMPLATE ENABLED:",
//   //             config.nf_custom_receipt_template
//   //         );
//   //         console.log(
//   //             "NF TEMPLATE ID:",
//   //             config.nf_receipt_template_id
//   //         );

//   //         data.extra_data = {
//   //             ...data.extra_data,

//   //             nf_custom_receipt_template_enabled:
//   //                 !!config.nf_custom_receipt_template,

//   //             nf_receipt_template_id:
//   //                 config.nf_receipt_template_id || false,
//   //         };

//   //         console.log("FINAL EXTRA DATA:", data.extra_data);

//   //         return data;
//   //     },
// });


import { patch } from "@web/core/utils/patch";
import { globalTemplates } from "@odoo/owl";
import { GeneratePrinterData } from "@point_of_sale/app/utils/printer/generate_printer_data";

const registeredTemplates = new Set();

function registerDynamicReceiptTemplate(name, xmlContent) {
    if (registeredTemplates.has(name)) {
        return true;
    }
    const doc = new DOMParser().parseFromString(
        `<templates><t t-name="${name}">${xmlContent}</t></templates>`,
        "text/xml"
    );
    if (doc.getElementsByTagName("parsererror").length) {
        console.error(
            "[nf_custom_receipt] Invalid XML in custom receipt template:",
            doc.getElementsByTagName("parsererror")[0].textContent
        );
        return false;
    }
    globalTemplates[name] = doc.querySelector("[t-name]");
    registeredTemplates.add(name);
    console.log("[nf_custom_receipt] Registered template:", name);
    return true;
}

patch(GeneratePrinterData.prototype, {
    generateReceiptData() {
        const data = super.generateReceiptData(...arguments);
        try {
            const template = this.config.nf_custom_receipt_template && this.config.nf_receipt_template_id;
            if (template && template.nf_receipt_xml) {
                const version = template.write_date ? new Date(template.write_date).getTime() : template.id;
                const templateName = `nf_pos_custom_receipt.nf_receipt_template_${template.id}_${version}`;
                const ok = registerDynamicReceiptTemplate(templateName, template.nf_receipt_xml);
                data.extra_data.nf_custom_receipt_template_name = ok ? templateName : false;
                if (!ok) {
                    console.warn("[nf_custom_receipt] Falling back to default receipt: template XML failed to register.");
                }
            } else {
                data.extra_data.nf_custom_receipt_template_name = false;
            }
        } catch (e) {
            console.error("[nf_custom_receipt] generateReceiptData override crashed, falling back to default receipt:", e);
            data.extra_data.nf_custom_receipt_template_name = false;
        }
        return data;
    },
});