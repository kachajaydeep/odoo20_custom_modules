import {Component, onWillStart, proxy, onMounted} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {registry} from "@web/core/registry";
import {formatCurrency} from "@web/core/currency";

var GenderWiseOrders = {
    annotations: {
        position: "back",
    },
    dataLabels: {
        enabled: false,
    },
    chart: {
        type: "bar",
        height: 400,
    },
    fill: {
        opacity: 1,
    },
    plotOptions: {},
    series: [
        {
            name: "Gender",
            data: [0, 0],
        },
    ],
    colors: "#435ebe",
    xaxis: {
        categories: ["Male", "Female"],
    },
    options: {
        responsive: true,
    },
};
var config4 = {
  chart: {
    type: "line",
    height: 400,
  },
  series: [
    {
      name: "sales",
      data: [],
    },
  ],
  xaxis: {
    categories: [],
  },
}

export class TailorDashboard extends Component {
    setup() {
        var self = this;
        this.orm = useService("orm");
        this.user = "";
        this.get_selling_amount = 0.0;
        this.counter_card_details = {};
        this.state = proxy({
            user_img: "",
            start_date: "",
            end_date: "",
            total_order_count: 0,
            inprogres_orders_count: 0,
            new_orders_count: 0,
            done_orders: 0,
            cancel_orders: 0,
            confirmed_orders: 0,
            gender_chart: "month",
            invoice_chart: "month",
            pending_order: [],
            delievered_order_list: [],
            recent_customer_list: [],
            invoice_list: [],
        });

        onWillStart(async () => {
            //Calculate Date
            await this.set_start_end_date();
            //get data from backed
            this.counter_card_details = await this.get_counter_card_details();

            console.log("user check ???");
            // Get User Info
            this.user = this.counter_card_details.user;
            
            this.state.user_img = `/web/image?model=res.users&field=avatar_1920&id=${this.user.id}`;

            // get total oder
            this.get_selling_amount = await formatCurrency(
                this.counter_card_details.sale_amount,
                this.user.currency_id[0]
            );

            this.state.total_order_count = this.counter_card_details.total_order_count;
            this.state.inprogres_orders_count = this.counter_card_details.inprogres_orders_count;
            this.state.new_orders_count = this.counter_card_details.new_orders_count;
            this.state.confirmed_orders = this.counter_card_details.confirmed_orders;
            this.state.done_orders = this.counter_card_details.done_orders;
            this.state.cancel_orders = this.counter_card_details.cancel_orders;
            this.state.pending_order = this.counter_card_details.pending_delievery_list;
            this.state.delievered_order_list = this.counter_card_details.delievered_order_list;
            this.state.recent_customer_list = this.counter_card_details.recent_customer_list;
            this.state.invoice_list = this.counter_card_details.invoice_list;
        });

        onMounted(async () => {
            this.onChangeGenderFilter();
            this.onChangeInvoiceFilter();
        });
    }

    convert_amount(amount){
        return formatCurrency(
                amount,
                this.user.currency_id[0]
            );
    }
    view_invoice(id){
        return this.orm.call(
            "nf.tailor.order",
            "nf_open_invoice",
            [id,]
        );
    }
    async onchangeStartDate(){
        this.counter_card_details = await this.get_counter_card_details();
 
        // get total oder
        this.get_selling_amount = await formatCurrency(
            this.counter_card_details.sale_amount,
            this.user.currency_id[0]
        );

        this.state.total_order_count = this.counter_card_details.total_order_count;
        this.state.inprogres_orders_count = this.counter_card_details.inprogres_orders_count;
        this.state.new_orders_count = this.counter_card_details.new_orders_count;
        this.state.confirmed_orders = this.counter_card_details.confirmed_orders;
        this.state.done_orders = this.counter_card_details.done_orders;
        this.state.cancel_orders = this.counter_card_details.cancel_orders;
        this.state.pending_order = this.counter_card_details.pending_delievery_list;
        this.state.delievered_order_list = this.counter_card_details.delievered_order_list;
        this.state.recent_customer_list = this.counter_card_details.recent_customer_list;
        this.state.invoice_list = this.counter_card_details.invoice_list;
        
        this.onChangeGenderFilter();
        this.onChangeInvoiceFilter();
        this.render(true)
    }

    async get_pendding_orders(){
        const pending_order = await this.orm.call(
            "nf.tailor.order",
            "get_pending_deliverys",
            [
                this.state.start_date,
                this.state.end_date,
             ]
        );
                
    }

    
    async onChangeInvoiceFilter(){
        const invoice_data = await this.get_invoice_data_fom_model();
        config4.series[0].data = [];
        config4.xaxis.categories = [];
        if (this.state.invoice_chart == 'day'){
            await invoice_data.Sales_Data.forEach((ele) => {
                config4.series[0].data.push(ele.orderTotal);
                config4.xaxis.categories.push(ele.time);
            });
    
            document.getElementById("nf-tailor-invoice-chart").innerHTML = "";
            var InvoiceOrderChart = new ApexCharts(
                document.getElementById("nf-tailor-invoice-chart"),
                config4
            );
            InvoiceOrderChart.render();

        } else if (this.state.invoice_chart == 'month'){
            await invoice_data.Sales_Data.forEach((ele) => {
                config4.series[0].data.push(ele.Amount);
                config4.xaxis.categories.push(ele.day);
            });
    
            document.getElementById("nf-tailor-invoice-chart").innerHTML = "";
            var InvoiceOrderChart = new ApexCharts(
                document.getElementById("nf-tailor-invoice-chart"),
                config4
            );
            InvoiceOrderChart.render();

        }else{
            await invoice_data.Sales_Data.forEach((ele) => {
                config4.series[0].data.push(ele.Amount);
                config4.xaxis.categories.push(ele.month);
            });

            document.getElementById("nf-tailor-invoice-chart").innerHTML = "";
            var InvoiceOrderChart = new ApexCharts(
                document.getElementById("nf-tailor-invoice-chart"),
                config4
            );
            InvoiceOrderChart.render();
        }

    }
    async get_invoice_data_fom_model(){
        return await this.orm.call(
            "nf.tailor.order",
            "get_invoice_model",
            [
                this.state.start_date,
                this.state.end_date,
                this.state.invoice_chart,
            ]
        );

    }
    async get_gender_data_fom_model() {
        
        return await this.orm.call(
            "nf.tailor.order",
            "get_gender_data_fom_model",
            [
                this.state.start_date,
                this.state.end_date,
                this.state.gender_chart,
            ]
        );
    }
    async onChangeGenderFilter(event) {
        const gender_data = await this.get_gender_data_fom_model();
        GenderWiseOrders.series[0].data = [];
        GenderWiseOrders.xaxis.categories = [];
        await gender_data.forEach((ele) => {
            GenderWiseOrders.series[0].data.push(ele.count);
            GenderWiseOrders.xaxis.categories.push(ele.gender);
        });
        document.getElementById("nf-tailor-gender-chart").innerHTML = "";
        var GenderOrderChart = new ApexCharts(
            document.getElementById("nf-tailor-gender-chart"),
            GenderWiseOrders
        );
        GenderOrderChart.render();
        this.render()
    }
    async set_start_end_date() {
        let date = new Date();
        let stat_Date = new Date(date.getFullYear(), date.getMonth(), 1);
        this.state.start_date = stat_Date.toLocaleDateString("en-CA", {
            timeZone: this.user.tz,
        });
        this.state.end_date = new Date().toISOString().split("T")[0];
    }
    async get_counter_card_details() {
        return await this.orm.call(
            "nf.tailor.order",
            "get_counter_card_details",
            [this.state.start_date, this.state.end_date]
        );
    }
    get greeting() {
        const hour = new Date().getHours();
        return hour < 12 ? "Morning" : hour < 18 ? "Afternoon" : "Evening";
    }
}
TailorDashboard.template = "nf_tailor_management.TailorDashboard";
registry
    .category("actions")
    .add("nf_tailor_dashboard_dashboard", TailorDashboard, {force: true});
