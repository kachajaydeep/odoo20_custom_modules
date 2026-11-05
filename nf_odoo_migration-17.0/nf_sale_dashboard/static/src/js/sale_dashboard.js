/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useInputField } from "@web/views/fields/input_field_hook";
import { session } from "@web/session";

import { Component, onMounted, useState } from "@odoo/owl";


let PaymentDataPieChart = {
    series: [],
    labels: [],
    colors: ['#435ebe', '#55c6e8', '#bd4a07', '#e3e306', '#28e306', '#34302e', '#00ff95', '#e400ff0'],
    chart: {
        type: 'donut',
        width: '100%',
        height: '350px'
    },
    legend: {
        position: 'bottom'
    },
    plotOptions: {
        pie: {
            donut: {
                size: '30%'
            }
        }
    }
}

var SelectedDaySaleData = {
    annotations: {
        position: 'back'
    },
    dataLabels: {
        enabled: false,
    },
    chart: {
        type: 'bar',
        height: 300
    },
    yaxis: {
        title: {
            text: " Sales ",
        },
    },
    fill: {
        opacity: 1
    },
    plotOptions: {},
    series: [{
        title: 'sales',
        data: []
    }],
    colors: '#435ebe',
    xaxis: {
        title: {
            text: " Date ",
        },
        categories: [],
    },
}

export class NfSaleDashboard extends Component {
    static template = "nf_sale_dashboard_template";
    setup() {
        var self = this;
        this.orm = useService('orm');
        this.user = this.get_currentuser()
        this._loadData();
    }
    async _loadData() {
        var self = this;
        await this.orm.call('sale.order', 'search_read', []).then(function (result) {
            self.sale_orders = result;
            self._render();
        })
    }
    async get_currentuser() {
        var self = this;
        var user = await this.orm.call('sale.order', 'search_read', []).then(function (user) {
            self.user = user
            self.render()
        })
        return user
    }
    get_user_avtar() {
        // var user = this.get_currentuser()
        return `/web/image?model=res.users&field=avatar_128&id=${session.user_id[0]}`
    }
    _render() {
        console.log('>>>>>>>>>>>>>>>> ', this);
        // this.$el.html(core.qweb.render('nf_sale_dashboard_template', {
        //     sale_orders: this.sale_orders,
        // }));
    }
}
registry.category("actions").add("nfsaledashboardtemplate", NfSaleDashboard);
