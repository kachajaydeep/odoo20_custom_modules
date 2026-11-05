    import { _t } from "@web/core/l10n/translation";
    import {Component, onMounted, useRef,useProps, proxy, t} from "@odoo/owl";
    import { Dialog } from "@web/core/dialog/dialog";
    import { usePos } from "@point_of_sale/app/hooks/pos_hook";
    import { useService } from "@web/core/utils/hooks";

    export class NfStockRequestPopup extends Component {
        static template = "nf_pos_stock_request.NfStockRequestPopup";
        static components = { Dialog };

        static props = {
            quants: { type: Array, optional: true },
            cancelText: { type: String, optional: true },
            confirmText: { type: String, optional: true },
            title: { type: String, optional: true },
        };
        setup() { 
            super.setup();
            this.pos = usePos();
            const quantity = this.pos.getOrder().getSelectedOrderline().getQuantity();
            this.notification = useService("notification");

            this.state = proxy({
                quants: this.props.quants.filter((quant) => quant.quantity >= quantity),
                request_quantity: quantity,
            });
            this.orm = useService("orm")
        };
        async generateInternalTransfer(quant){
             const quantity = parseFloat(this.state.request_quantity) || 0;
            if (quantity <= 0) {
                return this.notification.add(_t("Please enter a valid quantity."), { type: "danger" });
            }
            
            const pickingcontext = {
                picking_type_id: this.pos.config.picking_type_id.id,
                location_id: quant.location_id[0],
                location_dest_id: this.pos.config.picking_type_id.default_location_src_id.id,
                nf_pos_config_id:this.pos.config.id,

            }
            const stock_move_context = {
                product_id: quant.product_id[0],
                product_uom_qty:quantity,
            }
            const picking = await this.orm.call("stock.picking","create_from_pos",[],
                {
                    context: {
                        pickingcontext: pickingcontext,
                        stock_move_context: stock_move_context
                    }
                }
            )

            this.props.getPayload(quant);
            this.props.close();
        }
        cancel(){
            this.props.close();
        }
    }
