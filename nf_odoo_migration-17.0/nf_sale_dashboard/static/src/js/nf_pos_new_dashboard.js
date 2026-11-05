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

export class POSDashboard extends Component {
    static template = "NfDashboard";
    static props = ["*"];
    setup() {
        var self = this;
        this.orm = useService('orm');
        this.Company_id = false;
        const currentCompanyId = session.user_companies.current_company;
        const currentCompany = session.user_companies.allowed_companies[currentCompanyId];
        this.Company_id = currentCompany.id
        this.user = this.get_currentuser()

        this.getTodayOrder(this.Company_id)
        this.getTopCustomer(this.Company_id)
        this.getAllOrderData(this.Company_id)
        this.GetPaymentData(this.Company_id)
        this.GetStockData(this.Company_id)
        onMounted(() => {
            this.getTotalSaleDataForChart($('#NfSaleFilter').val(), self.Company_id)
            $('#NfSaleFilter').change(function(event) {
                $('.nf-pos-month-sale-chart').empty()
                self.getTotalSaleDataForChart($(event.target).val(), self.Company_id)
            })
            $('.Click_product_sold').click(function(ev) {
                $('#dashboard_counter').toggleClass('NfProductData')
                self.getSaleProductDate(self.Company_id)
            })
            $('.nf-times').click(function(ev) {
                $('#dashboard_counter').removeClass('NfProductData')
                $('.product-data-table').find('tbody').empty()
            })
        })

    }
    async get_currentuser() {
        var self = this;
        var user = await this.orm.call('nf.pos.dashboard', 'get_current_user', []).then(function (user) {
            self.user = user
            self.render()
        })
        return user
    }
    get_user_avtar() {
        // var user = this.get_currentuser()
        return `/web/image?model=res.users&field=avatar_128&id=${session.user_id[0]}`
    }
    async getTodayOrder(Company_id) {
        var self = this;
        const date = new Date();
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');

        const Today = `${year}-${month}-${day}`;
        await this.orm.call('pos.order', 'search_read', [], {
            domain: [
                ['company_id', '=', Company_id],
                ['date_order', 'ilike', '%' + Today + '%']
            ],
        }).then(function(Order) {
            if (Order) {
                $('#nf-today-orders').text(Order.length)
            }
        })
    }
    getAllOrderData(Company_id) {
        var self = this;
        this.orm.call('nf.pos.dashboard', 'get_all_pos_order_data', [Company_id], 
        ).then(function(Orders) {
            if (Orders) {
                $('#nf-today-total-sales').text(Orders.currency_symbol + ' ' + Orders.Today_total_sale)
                $('#nf-today-product-sales').text(Orders.today_product_sold)
                $('#nf-pos-active-sessions').text(Orders.Total_active_sessions)
                $('.nf_top_sale_of_the_day').text(Orders.currency_symbol + ' ' + Orders.max_order_total)
                $('.nf_highest_of_month').text(Orders.currency_symbol + ' ' + Orders.heights_month_sale)
                $('.month_sale').text(Orders.currency_symbol + ' ' + Orders.month_sale)
                $('.nf_avarage_sale_of_month').text(Orders.currency_symbol + ' ' + Orders.avrage_salling_amount)
                $('.currency_icon').text(Orders.currency_symbol)
            }
        })
    }
    getTotalSaleDataForChart(Value, company_id) {
        var self = this;
        const date = new Date();
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');

        const today = `${year}-${month}-${day}`;

        var last_day = date.setDate(date.getDate() - 7);
        last_day = new Date(last_day)
        const lastyear = last_day.getFullYear();
        const lastmonth = String(last_day.getMonth() + 1).padStart(2, '0');
        const lastday = String(last_day.getDate()).padStart(2, '0')
        const last_today_day = `${lastyear}-${lastmonth}-${lastday}`;


        this.orm.call('nf.pos.dashboard', 'get_moth_sale_data_for_chart', [today, last_today_day, Value, company_id]).then(async function(OrderDataByMonth) {
            // get moths Chart 
            SelectedDaySaleData.series[0].data = []
            SelectedDaySaleData.xaxis.categories = []
            SelectedDaySaleData.yaxis.title = { text: "Sales (" + OrderDataByMonth.Currency_symbol + ")" }
            await OrderDataByMonth.Sales_Data.forEach(eachhour => {
                if (Value == 'Day') {
                    SelectedDaySaleData.xaxis.title = { text: "Time (hour)" }
                    SelectedDaySaleData.series[0].data.push(eachhour.orderTotal)
                    SelectedDaySaleData.xaxis.categories.push(eachhour.time)
                } else if (Value == 'Year') {
                    SelectedDaySaleData.xaxis.title = { text: "Months" }
                    SelectedDaySaleData.series[0].data.push(eachhour.Amount)
                    SelectedDaySaleData.xaxis.categories.push(eachhour.month)
                } else if (Value == 'Month') {
                    SelectedDaySaleData.xaxis.title = { text: "Date (Days)" }
                    SelectedDaySaleData.series[0].data.push(eachhour.Amount)
                    SelectedDaySaleData.xaxis.categories.push(eachhour.day)
                }
            })

            var chartProfileVisit = new ApexCharts($('.nf-pos-month-sale-chart')[0], SelectedDaySaleData);

            chartProfileVisit.render();

        })
    }
    getSaleProductDate(company_id) {
        var self = this;
        this.orm.call('nf.pos.dashboard','getSaleProductDate',[company_id]).then(async function(Data) {

            await Data.forEach(data => {
                $('.product-data-table').find('tbody').append("<tr><td style='padding: 10px;'>" + data[0] + "</td><td style='padding: 10px;'>" + data[1][session.bundle_params.lang] + "</td><td style='padding: 10px;'>" + data[2] + "</td><td style='padding: 10px;'>" + data[3] + "</td> <tr>")
            })

        })
    }
    getTopCustomer(company_id) {
        var self = this;
        this.orm.call('nf.pos.dashboard','get_top_customer_data',[company_id]).then(function(Customer) {

            Customer.PartnerData.forEach(cust => {
                var div = " <tr> <td> " + cust.partner_name + "</td> <td> " + cust.total_product + " </td> <td> " + Customer.currency_symbol + " " + cust.amount + " </td> </tr> "

                $('.NF-Customer-Data').append(div)
            })
        })
    }
    GetPaymentData(company_id) {
        var self = this
        this.orm.call('nf.pos.dashboard','GetThisMonthPaymentData',[company_id]).then(async function(OrderDataByMonth) {
            PaymentDataPieChart.series = []
            PaymentDataPieChart.labels = []
            await OrderDataByMonth.forEach(month => {
                PaymentDataPieChart.series.push(month.amount)
                PaymentDataPieChart.labels.push(month.payment_name[session.bundle_params.lang] )
            })
            var chartVisitorsProfile = new ApexCharts($('#chart-profile-visit')[0], PaymentDataPieChart)
            chartVisitorsProfile.render()
        })
    }
    GetStockData (company_id) {
        var self = this;
        this.orm.call('nf.pos.dashboard','GetStockData',[company_id]).then(function(Datas) {

            Datas.forEach(data => {
                var div = " <tr> <td> " + data.product_name[session.bundle_params.lang] + "</td> <td> " + data.total_qty + " </td> <td> " + data.totalamount + " </td>  </tr> "

                $('.nf-stock-update').append(div)
            })

        })
    }
}


registry.category("actions").add("nf_pos_dashboard_design", POSDashboard);
// return {
//     POSDashboard: POSDashboard,
// };

// export const POSDashboard = {
//     component: POSDashboard,
// };

