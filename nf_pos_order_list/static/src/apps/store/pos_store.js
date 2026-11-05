import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {
    async setup() {
        await super.setup(...arguments)
        var self = this;
        this.ORDERLIST_SCREEN_STATE = {
            syncedOrders: {
                currentPage: 1,
                cache: {},
                toShow: [],
                nPerPage: self.config.nf_pos_order_limit_per_page,
                totalCount: 0,
                cacheDate: {},
            },
            ui: {
                selectedOrder: null,
                searchDetails: this.getDefaultSearchDetails(),
                filter: null,
                // maps the order's backendId to it's selected orderline
                selectedOrderlineIds: {},
                highlightHeaderNote: false,
            },
        }  
    },
    // async _processData(loadedData) {
    //     await super._processData(...arguments);
    //     this.nf_pos_order_by_id = loadedData['nf_pos_order_by_id']
    // },
    // showBackButton() {
    //     var res = super.showBackButton()        
    //     return (res  || this.mainScreen.component === NfOrderListScreen )
    // }
})