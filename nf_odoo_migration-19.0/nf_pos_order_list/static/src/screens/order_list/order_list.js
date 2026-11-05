import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { SearchBar } from "@point_of_sale/app/screens/ticket_screen/search_bar/search_bar";
// import { usePos } from "@point_of_sale/app/store/pos_hook";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
// import { nfPosOrderLinesPopup } from "@nf_pos_order_list/apps/popups/nf_order_lines/nf_order_lines_popup";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { Component, onMounted, useState } from "@odoo/owl";

export class NfOrderListScreen extends Component {
    static storeOnOrder = false;
    static template = "nf_pos_order_list.NfOrderListScreen";
    static components = {
        SearchBar,
    };
    static searchPlaceholder = _t("Search Orders...");
    async setup() {
        this.pos = usePos();
        this.ui = useState(useService("ui"));
        this.orm = useService("orm");
        this.dialog = useService("dialog");
        
        this._state = useState(this.pos.ORDERLIST_SCREEN_STATE);
        onMounted(this.onMounted);

        Object.assign(this._state.ui, this.props.ui || {});
    }
    onMounted() {
        setTimeout(() => {
            // Show updated list of synced orders when going back to the screen.
            this.onFilterSelected(this._state.ui.filter);
        });
    }
    async nfReorder(order){
        var self = this;
        [...this.pos.get_order().get_orderlines()].map(async (line) => await this.pos.get_order().removeOrderline(line))

        var currentOrder = this.pos.get_order()

        if (order.get_partner()){
            await currentOrder.set_partner(order.get_partner())
        }

        console.log(order.lines);
        if( order.lines ){
            
            [...order.lines].map(async (line) => await self.pos.addLineToCurrentOrder({ product_id: line.product_id }, {}, false))

        }
        this.closeOrderListScreen()
    }
    async nfDisplayLines( order ){
        let orderLines = order.get_orderlines()
        await makeAwaitable(this.dialog, nfPosOrderLinesPopup, { lines: orderLines, 'total_tax': order.amount_tax, 'order_total': order.amount_total, 'total_paid': order.amount_paid, title: _t("Order Line information") });
    }
    async onClickOrder(clickedOrder){
        this._state.ui.selectedOrder = clickedOrder;
    }
    async onFilterSelected(selectedFilter) {
        this._state.ui.filter = selectedFilter;
        await this._fetchSyncedOrders();
    }
    closeOrderListScreen() {
        this.pos.navigate("ProductScreen", {
            orderUuid: this.pos.selectedOrderUuid,
        });
    }
    getFilteredOrderList() {
        return this._state.syncedOrders.toShow || [];
    }
    getSelectedOrder() {
        if (this._state.ui.filter == "SYNCED" && this._state.ui.selectedOrder) {
            return this._state.syncedOrders.cache[
                this._state.ui.selectedOrder.backendId
            ];
        } else {
            return this._state.ui.selectedOrder;
        }
    }
    isHighlighted(order) {
        const selectedOrder = this.getSelectedOrder();

        return selectedOrder
            ? (order.backendId && order.backendId == selectedOrder.backendId) ||
                  order.uuid === selectedOrder.uuid
            : false;
    }
    nfGetSearchData() {
        console.log({
            searchFields: new Map(
                Object.entries(this._getSearchFields()).map(([key, val]) => [
                    key,
                    val.displayName,
                ])
            ),
            filter: { show: true, options: this._getFilterOptions() },
            defaultSearchDetails: this._state.ui.searchDetails,
            defaultFilter: this._state.ui.filter,
        });
        
        return {
            searchFields: new Map(
                Object.entries(this._getSearchFields()).map(([key, val]) => [
                    key,
                    val.displayName,
                ])
            ),
            filter: { show: true, options: this._getFilterOptions() },
            defaultSearchDetails: this._state.ui.searchDetails,
            defaultFilter: this._state.ui.filter,
        };
    }
    _getFilterOptions() {
        const orderStates = this._getOrderStates();
        orderStates.set("SYNCED", { text: _t("All Orders") });
        return orderStates;
    }
    _getSearchFields() {
        const fields = {
            TRACKING_NUMBER: {
                repr: (order) => order.trackingNumber,
                displayName: _t("Order Number"),
                modelField: "tracking_number",
            },
            RECEIPT_NUMBER: {
                repr: (order) => order.name,
                displayName: _t("Receipt Number"),
                modelField: "pos_reference",
            },
            DATE: {
                repr: (order) =>
                    deserializeDate(order.date_order).toFormat(
                        "yyyy-MM-dd HH:mm a"
                    ),
                displayName: _t("Date"),
                modelField: "date_order",
            },
            PARTNER: {
                repr: (order) => order.get_partner_name(),
                displayName: _t("Customer"),
                modelField: "partner_id.complete_name",
            },
        };
        return fields;
    }
    getDate(order) {
        return formatDateTime(order.date_order);
    }
    getPartner(order) {
        if (order.get_partner()){
            return order.get_partner().name
        }else{
            return ''
        }
    }
    getCashier(order) {
        return order.cashier ? order.cashier.name : "";
    }
    getTotal(order) {
        if (order.get_total_with_tax()){
            return this.env.utils.formatCurrency(order.get_total_with_tax());
        } else{
            return 0.00
        }
    }
    getStatus(order) {
        return _t(order.state);
    }
    nfPagination() {
        return this._getLastPage() > 1;
    }
    async onNextPage() {
        if (this._state.syncedOrders.currentPage < this._getLastPage()) {
            this._state.syncedOrders.currentPage += 1;
            await this._fetchSyncedOrders();
        }
    }
    async onPrevPage() {
        if (this._state.syncedOrders.currentPage > 1) {
            this._state.syncedOrders.currentPage -= 1;
            await this._fetchSyncedOrders();
        }
    }
    getPageNumber() {
        if (!this._state.syncedOrders.totalCount) {
            return `1/1`;
        } else {
            return `${this._state.syncedOrders.currentPage}/${this._getLastPage()}`;
        }
    }
    _getLastPage() {
        const totalCount = this._state.syncedOrders.totalCount;
        const nPerPage = this._state.syncedOrders.nPerPage;
        const remainder = totalCount % nPerPage;
        if (remainder == 0) {
            return totalCount / nPerPage;
        } else {
            return Math.ceil(totalCount / nPerPage);
        }
    }
    async onSearch(search) {        
        Object.assign(this._state.ui.searchDetails, search);
        this._state.syncedOrders.currentPage = 1;
        await this._fetchSyncedOrders();
    }
    _computeSyncedOrdersDomain() {
        const { fieldName, searchTerm } = this._state.ui.searchDetails;
        const { filter } = this._state.ui;

        const searchField = this._getSearchFields()[fieldName];
        if (searchField && searchField?.modelField && searchField?.modelField !== null && searchTerm != "") {
            if (searchField.formatSearch) {
                searchTerm = searchField.formatSearch(searchTerm);
            }
            return [[searchField.modelField, "ilike", `%${searchTerm}%`]];
        }

        var domain = [];

        if (filter == "DONE") {
            domain.push(["state", "=", "done"]);
        } else if (filter == "INVOICED") {
            domain.push(["state", "=", "invoiced"]);
        } else if (filter == "PAID") {
            domain.push(["state", "=", "paid"]);
        }
        if (!searchTerm) {
            return domain;
        }
        const modelField = this._getSearchFields()[fieldName].modelField;
        if (modelField) {
            domain.push([modelField, "ilike", `%${searchTerm}%`])
            return domain
        } else {
            return domain;
        }
    }
    async _fetchSyncedOrders() {
        const domain = this._computeSyncedOrdersDomain();
        const limit = this._state.syncedOrders.nPerPage;
        const offset = (this._state.syncedOrders.currentPage - 1) * this._state.syncedOrders.nPerPage;
        const config_id = this.pos.config.id;
        
        const { ordersInfo, totalCount } = await this.orm.call(
            "pos.order",
            "search_paid_order_ids",
            [],
            { config_id, domain, limit, offset }
        );
        var orders = []
        if (ordersInfo && ordersInfo.length){
            let order_ids = ordersInfo.map((x) => x[0])
            console.log('order_ids',order_ids);
            orders = await this.pos.models["pos.order"].filter((x) => order_ids.includes(x.id)).sort((a, b) => b.id - a.id);
            console.log('====?>',orders);
            
        }else{
            orders = this.pos.models["pos.order"].getAll();
        }
        
        this._state.syncedOrders.totalCount = totalCount;
        this._state.syncedOrders.toShow = orders
    }
    _getOrderStates() {
        const states = new Map();
        states.set("DONE", {
            text: _t("Done"),
        });
        states.set("PAID", {
            text: _t("Paid"),
        });
        states.set("INVOICED", {
            text: _t("Invoiced"),
        });
        return states;
    }
}

registry.category("pos_pages").add("NfOrderListScreen", {
    name: "NfOrderListScreen",
    component: NfOrderListScreen,
    route: `/pos/ui/${odoo.pos_config_id}/nforderlist`,
    params: {
        orderUuid: true,
        orderFinalized: false,
    },
});
