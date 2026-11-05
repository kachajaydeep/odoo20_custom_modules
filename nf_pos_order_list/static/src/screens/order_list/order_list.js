import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { formatDateTime } from "@web/core/l10n/dates";
import { _t } from "@web/core/l10n/translation";
import { SearchBar } from "@point_of_sale/app/screens/ticket_screen/search_bar/search_bar";
import { nfPosOrderLinesPopup } from "@nf_pos_order_list/apps/popups/nf_order_lines/nf_order_lines_popup";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { Component, onMounted, proxy } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

export class NfOrderListScreen extends Component {
    static storeOnOrder = false;
    static template = "nf_pos_order_list.NfOrderListScreen";
    static components = {
        SearchBar,
    };
    setup() {
        this.ui = proxy(useService("ui"));
        this.orm = useService("orm");
        this.pos = usePos()
        this.dialog = useService("dialog");
        this._state = proxy(this.pos.ORDERLIST_SCREEN_STATE);
        onMounted(this.onMounted);
        Object.assign(this._state.ui, this.props.ui || {});
        this._state.ui.filter = 'SYNCED';         
    }
    onMounted() {
        this._fetchSyncedOrders();
    }

    async nfReorder(order) {
        var self = this;
        if (!this.pos.getOrder()){
            this.pos.createOrder();
        }

        [...this.pos.getOrder().getOrderlines()].map(
            async (line) => await this.pos.getOrder().removeOrderline(line)
        );

        const currentOrder = this.pos.getOrder();
        if (order.getPartner()) {
            await currentOrder.setPartner(order.getPartner());
        }
        if (order.lines) {
            [...order.lines].map(
                async (line) => await self.pos.addLineToCurrentOrder(
                    {
                        product_id: line.product_id,
                        product_tmpl_id: line.product_id.product_tmpl_id
                    },
                    { },
                    false
                )
            );
        }
        this.closeOrderListScreen();
    }

    async nfDisplayLines(order) {
        let orderLines = order.getOrderlines();
        await makeAwaitable(this.dialog, nfPosOrderLinesPopup, {
            title: _t("Order Line information"),
            lines: orderLines,
            total_tax: order.amount_tax,
            order_total: order.amount_total,
            total_paid: order.amount_paid,
        });
    }

    async onClickOrder(clickedOrder) {
        this._state.ui.selectedOrder = clickedOrder;
    }

    async onFilterSelected(selectedFilter) {
        this._state.ui.filter = selectedFilter;
        this._state.syncedOrders.currentPage = 1;
        this._state.ui.selectedOrder = null;
        await this._fetchSyncedOrders();
    }

    closeOrderListScreen() {
        this.pos.navigate("ProductScreen", { orderUuid: this.pos.getOrder()?.uuid });
    }

    getFilteredOrderList() {
        return this._state.syncedOrders.toShow;    
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
        return {
            searchFields: new Map(
                Object.entries(this._getSearchFields()).map(([key, val]) => [
                    key,
                    val.displayName,
                ])
            ),
            filter: {show: true, options: this._getFilterOptions()},
            defaultSearchDetails: this._state.ui.searchDetails,
            defaultFilter: this._state.ui.filter,
        };
    }

    _getFilterOptions() {
        const orderStates = this._getOrderStates();
        orderStates.set("SYNCED", {text: _t("All Orders")});
        return orderStates;
    }

    _getSearchFields() {
        return {
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
                repr: (order) => this.getDate(order),
                displayName: _t("Date"),
                modelField: "date_order",
            },
            PARTNER: {
                repr: (order) => order.get_partner_name(),
                displayName: _t("Customer"),
                modelField: "partner_id.complete_name",
            },
        };
    }

    getDate(order) {
        return formatDateTime(order.date_order);
    }

    getPartner(order) {
        return order.getPartner() ? order.getPartner().name : "";
    }

    getCashier(order) {
        return order.cashier ? order.cashier.name : "";
    }

    getTotal(order) {
        return order.amount_total ? order.amount_total.toFixed(2) : "0.00";
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
        const last = this._getLastPage();
        return `${this._state.syncedOrders.currentPage}/${last || 1}`;
    }

    _getLastPage() {
        const { totalCount, nPerPage } = this._state.syncedOrders;
        if (!totalCount) return 1;
        return Math.ceil(totalCount / nPerPage);
    }

    async onSearch(search) {
        Object.assign(this._state.ui.searchDetails, search);
        this._state.syncedOrders.currentPage = 1;
        this._state.ui.selectedOrder = null;
        await this._fetchSyncedOrders();
    }

    _computeSyncedOrdersDomain() {
        const { fieldName, searchTerm } = this._state.ui.searchDetails;
        const { filter } = this._state.ui;
        const domain = [];

        if (filter === "DONE") {
            domain.push(["state", "=", "done"]);
        } else if (filter === "INVOICED") {
            domain.push(["state", "=", "invoiced"]);
        } else if (filter === "PAID") {
            domain.push(["state", "=", "paid"]);
        }
        if (searchTerm) {
            const searchField = this._getSearchFields()[fieldName];
            if (searchField && searchField.modelField) {
                domain.push([searchField.modelField, "ilike", `%${searchTerm}%`]);
            }
        }

        return domain;
    }

    async _fetchSyncedOrders() {
        const domain = this._computeSyncedOrdersDomain();
        const limit = this._state.syncedOrders.nPerPage;
        const offset = (this._state.syncedOrders.currentPage - 1) * limit;
        const config_id = this.pos.config.id;
        
        const result = await this.orm.call(
            "pos.order",
            "nf_pos_get_all_orders",
            [[], domain, limit, offset, config_id]
        );
        const orderIds = result.ids || [];
        const totalCount = result.total || 0;
        this._state.syncedOrders.totalCount = totalCount;
        if (orderIds.length === 0) {
            this._state.syncedOrders.toShow = [];
            return;
        }

        // Load any missing orders from server into POS model cache
        await this.pos.data.loadServerOrders([["id", "in", orderIds]]);
        
        // fetch exactly the orders for this page in correct order
        const allLoaded = this.pos.models["pos.order"].getAll();
        
        const idSet = new Set(orderIds);
        const matched = allLoaded.filter((o) => idSet.has(o.id));

        // Sort by the server's returned id order
        const idIndex = Object.fromEntries(orderIds.map((id, i) => [id, i]));
        matched.sort((a, b) => idIndex[a.id] - idIndex[b.id]);
        
        this._state.syncedOrders.toShow = matched.filter((o) => o.state !== 'draft');
    }
    
    _getOrderStates() {
        const states = new Map();
        states.set("DONE", { text: _t("Done") });
        states.set("PAID", { text: _t("Paid") });
        states.set("INVOICED", { text: _t("Invoiced") });
        return states;
    }
}

registry.category("pos_pages").add("NfOrderListScreen", {
    name: "NfOrderListScreen",
    component: NfOrderListScreen,
    route: `/pos/ui/${odoo.pos_config_id}/order_list_screen`,
    params: {},
});