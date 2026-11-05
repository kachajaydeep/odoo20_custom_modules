/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useInputField } from "@web/views/fields/input_field_hook";
import { session } from "@web/session";

import { Component, onWillStart, onMounted, proxy } from "@odoo/owl";


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

const SelectedDaySaleData = {
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

export class NfPOSDashboard extends Component {
    static template = "nf_pos_dashboard.NfDashboard";
    setup() {
        const self = this;
        this.orm = useService('orm');
        this.Company_id = false;

        onWillStart(async () => {
            this.Company_id = await this.orm.call(
                "nf.pos.dashboard",
                "nf_get_compnay_id"
            );
            let current_Date = new Date();
            let current_hour = current_Date.getHours();
            let current_minute = current_Date.getMinutes()
            if (Number(`${current_hour}.${current_minute} `)>= 5 && Number(`${current_hour}.${current_minute} `) < 12) {
                this.farewell = 'Good Morning';
            } else if (Number(`${current_hour}.${current_minute} `) >= 12 && Number(`${current_hour}.${current_minute} `) < 17) {
                this.farewell = 'Good Afternoon';
            } else if (Number(`${current_hour}.${current_minute} `) >= 17 && Number(`${current_hour}.${current_minute} `) < 19) {
                this.farewell = 'Good Evening';
            } else {
                this.farewell = 'Good Night';
            }
        });
        


        // Start Date
        this.start_date = new Date();
        this.start_date.setMonth(this.start_date.getMonth() - 1);
        const startYear = this.start_date.getFullYear();
        const startMonth = String(this.start_date.getMonth() + 1).padStart(2, '0');
        const startDay = String(this.start_date.getDate()).padStart(2, '0');
        const Start_date = `${startYear}-${startMonth}-${startDay}`;

        // End date: current date
        const endDateObj = new Date();
        const endYear = endDateObj.getFullYear();
        const endMonth = String(endDateObj.getMonth() + 1).padStart(2, '0');
        const endDay = String(endDateObj.getDate()).padStart(2, '0');
        const End_date = `${endYear}-${endMonth}-${endDay}`;

        this.session = session
        this.state =  proxy({ 
            start_date: Start_date ,end_date: End_date, nf_today_total_sales: '' ,
            today_product_sold : "",
            Total_active_sessions : "",
            max_order_total : "",
            heights_month_sale : "",
            month_sale : "",
            avrage_salling_amount : "",
            currency_symbol : "",
            order_length: 0,
            'top_customers': [],
            'nf_products': [],
            'Datas': [],
            user_img: ""
        });

        onMounted(async () => {
            this.user = this.get_currentuser();
            this.getTodayOrder(this.Company_id)
            this.getTopCustomer(this.Company_id)
            this.getAllOrderData(this.Company_id)
            this.GetPaymentData(this.Company_id)
            this.GetStockData(this.Company_id)
            this.getTotalSaleDataForChart('Month',self.Company_id)
        });

    }
    async NfSaleFilter(event){
        document.getElementsByClassName('nf-pos-month-sale-chart').innerHTML = '';
        this.getTotalSaleDataForChart(event.target.value, this.Company_id)
    }
    async get_currentuser() {
        const self = this;
        const user = await this.orm.call('nf.pos.dashboard', 'get_current_user', []).then(function (user) {
            self.user = user
            self.state.user_img = `/web/image?model=res.users&field=avatar_1920&id=${user.id}`
        })
        return user
    }
    _nfChangeDate(ev){
        this.getTodayOrder(this.Company_id)
        this.getAllOrderData(this.Company_id)
        this.getTotalSaleDataForChart('Month', this.Company_id)
    }
    async getTodayOrder(Company_id) {
        const self = this;
        if (this.state.start_date != "" && this.state.end_date != ""){
            await this.orm.call('pos.order', 'search_read', [], {
                domain: [
                    ['company_id', '=', Company_id],
                    ['date_order', '<=', this.state.end_date],
                    ['date_order', '>=', this.state.start_date]
                ],
            }).then(function(Order) {
                if (Order) {
                    self.state.order_length = Order.length
                }
            })
        }
    }
    getAllOrderData(Company_id) {
        const self = this;
        if (this.state.start_date != "" && this.state.end_date != ""){
            this.orm.call('nf.pos.dashboard', 'get_all_pos_order_data', [Company_id, this.state.start_date, this.state.end_date], 
            ).then(function(Orders) {
                if (Orders) {
                    self.state.nf_today_total_sales = Orders.currency_symbol + ' ' + Orders.Today_total_sale.toFixed(2)
                    self.state.today_product_sold = Orders.today_product_sold
                    self.state.Total_active_sessions = Orders.Total_active_sessions
                    self.state.max_order_total = Orders.currency_symbol + ' ' + Orders.max_order_total.toFixed(2)
                    self.state.heights_month_sale = Orders.currency_symbol + ' ' + Orders.heights_month_sale.toFixed(2)
                    self.state.month_sale = Orders.currency_symbol + ' ' + Orders.month_sale
                    self.state.avrage_salling_amount = Orders.currency_symbol + ' ' + Orders.avrage_salling_amount.toFixed(2)
                    self.state.currency_symbol = Orders.currency_symbol
                }
            })
        }
    }
    getTotalSaleDataForChart(Value, company_id) {
        const self = this;         
        if (this.state.start_date != "" && this.state.end_date != ''){
            this.orm.call('nf.pos.dashboard', 'get_moth_sale_data_for_chart', [ this.state.start_date, this.state.end_date, Value, company_id]).then(async function(OrderDataByMonth) {
                // get moths Chart 
                SelectedDaySaleData.series[0].data = []
                SelectedDaySaleData.xaxis.categories = []
                if (self.session.bundle_params.lang == "he_IL"){
                    SelectedDaySaleData.yaxis.title = { text: "מכירות" }
                }else{
                    SelectedDaySaleData.yaxis.title = { text: "Sales (" + OrderDataByMonth.Currency_symbol + ")" }
                }   
                if (OrderDataByMonth.Sales_Data){
    
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
    
                    document.getElementById('nf-pos-month-sale-chart').innerHTML = ""
                    const chartProfileVisit = new ApexCharts(document.getElementById('nf-pos-month-sale-chart'), SelectedDaySaleData);
        
                    chartProfileVisit.render();
                    self.render()
    
                    if (self.session.bundle_params.lang == "he_IL"){
                        const svgTextElements = document.querySelectorAll('.apexcharts-xaxis text')
                        svgTextElements.forEach(function (textElement) {
                            textElement.setAttribute('text-anchor', 'start');
                        });
                    }
                }
    
            })
        }
    }
    getSaleProductDate(company_id) {
        const self = this;
        this.orm.call('nf.pos.dashboard','getSaleProductDate',[company_id]).then(async function(Data) {
            self.state.Datas = Data;
        })
    }
    getTopCustomer(company_id) {
        const self = this;
        this.orm.call('nf.pos.dashboard','get_top_customer_data',[company_id]).then(function(Customer) {
            self.state.top_customers = Customer.PartnerData
        })
    }
    GetPaymentData(company_id) {
        const self = this
        if (this.state.start_date != "" && this.state.end_date != ""){
            this.orm.call('nf.pos.dashboard','GetThisMonthPaymentData',[company_id, this.state.start_date, this.state.end_date]).then(async function(OrderDataByMonth) {
                PaymentDataPieChart.series = []
                PaymentDataPieChart.labels = []
                await OrderDataByMonth.forEach(month => {
                    
                    PaymentDataPieChart.series.push(Number(month.amount))
                    PaymentDataPieChart.labels.push(month.payment_name[self.session.bundle_params.lang])
                })
                
                const chartVisitorsProfile = new ApexCharts(document.getElementById('chart-profile-visit'), PaymentDataPieChart);
                chartVisitorsProfile.render();
            })
        }
    }
    GetStockData (company_id) {
        const self = this;
        this.orm.call('nf.pos.dashboard','GetStockData',[company_id]).then(function(Datas) {
            self.state.nf_products = Datas
        })
    }
}


registry.category("actions").add("nf_pos_dashboard_template", NfPOSDashboard, { force: true });
