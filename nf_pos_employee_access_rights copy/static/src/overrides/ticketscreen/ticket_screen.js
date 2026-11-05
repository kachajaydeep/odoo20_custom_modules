import { patch } from "@web/core/utils/patch";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";

patch(TicketScreen.prototype, {
    _getFilterOptions() {
        var self = this;
        if (self.pos.getCashier() && self.pos.getCashier().nf_only_show_active_order){
            var res = super._getFilterOptions()
            var new_filter = new Map(res)
            new_filter.delete("SYNCED");
            return new_filter
        }else{
            return super._getFilterOptions()
        }
        
    }
})