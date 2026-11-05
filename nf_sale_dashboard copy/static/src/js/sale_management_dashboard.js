import { Component, onWillStart, proxy, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { formatCurrency } from "@web/core/currency";

var config4 = {
  chart: {
    type: "bar",
    height: 400,
  },
  plotOptions: {
    bar: {
      columnWidth: "150px"
    }
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
  colors: "#435ebe",
}
let sellingproductbyquantity = {
  series: [],
  labels: [],
  colors: [],
  chart: {
    type: "pie",
    width: "500",
    height: "500",
    toolbar: {
      show: true
    }
  },
  legend: {
    position:"right",
  },
  plotOptions: {
    pie: {
      // donut: {
      //   size: "30%",
      // },
    },
  },
  responsive: [
    {
      breakpoint: 768,
      options: {
        legend: {
          position: "bottom",
        },
        chart: {
          width: "100%",
        },
      },
    },
    {
      breakpoint: 480,
      options: {
        legend: {
          position: "bottom",
        },
      },
    },
  ],

}
let topCustomerRevenueChart = {
  series: [],
  labels: [],
  colors: [],
  chart: {
    type: "donut",
    width: "400",
    height: "400",
    toolbar: {
      show: true
    }
  },
  legend: {
    position: "right",
  },
  plotOptions: {
    pie: {
      donut: {
        size: "30%",
      },
    },
  },
  responsive: [
    {
      breakpoint: 768,
      options: {
        legend: {
          position: "bottom",
        },
        chart: {
          width: "100%",
        },
      },
    },
    {
      breakpoint: 480,
      options: {
        legend: {
          position: "bottom",
        },
      },
    },
  ],
}

export class SaleManagement extends Component {
  static template = "nf_sale_dashboard.SaleManagement";
  setup() {
    this.orm = useService("orm");
    this.user_name = "";
    this.user_img = "/web/image?model=res.users&field=avatar_1920&id=2";
    this.wish = "";
    const currentdateobject = new Date();
    const setnewDate = new Date(currentdateobject);
    setnewDate.setDate(1);
    this.productChart = null;
    this.customerRevenue = null;

    this.state = proxy({
      invoice_chart: "month",
      start_date:`${setnewDate.getFullYear()}-${setnewDate.getMonth() + 1}-0${setnewDate.getDate()}`,
      end_date:`${currentdateobject.getFullYear()}-${currentdateobject.getMonth() + 1}-${currentdateobject.getDate()}`,
      sale_order_record: [],
      user:{},
      sales_chart:"month",
      top_selling_products:[],
      top_customer_by_revenue:[],
      invoice_due_record:[],
      running_sale_order_record:[],
      pending_delivery_orders:[],
    });

    onWillStart(async () => {
      await this.saleOrders();
      await this.top_sale_orders();
      this.nf_set_start_end_date();
      await this.topProducts();
      await this.topCustomerByRevenue();
      await this.saleOrderPendingDeliveries();
    });

    onMounted(async () => {
      this.monthlySaleRecords();
      await this.onChangeSalesDetails();
      await this.productAnalysis();
      await this.customerAnalysisByRevenue();
    });

    this.orm = useService("orm");
  }

  async saleOrders() {
    const sale_order_record = await this.orm.call(
      "sale.order",
      "sale_Order_Record",
      [[]],
    );

    this.active_user_id = sale_order_record["user_details_obj"][0];
    console.log("this.active_user_id",this.active_user_id);
    this.state.user = this.active_user_id;
    this.user_name = this.active_user_id["name"];
    this.user_img = `/web/image?model=res.users&field=avatar_1920&id=${sale_order_record["user_details_obj"][0].id}`;
    this.avg_amount = sale_order_record["average_amount_obj"];
    this.avg_amount_with_currency = await formatCurrency(
      this.avg_amount,
      this.active_user_id.currency_id[0]
    )
    let currentdatetime = new Date();
    let currenthour = currentdatetime.getHours();
    let current_minute = currentdatetime.getTime();
    this.today_highest_sale = sale_order_record["today_highest_sale_object"];
    this.today_highest_sale_amount_with_currnecy = await formatCurrency(
      this.today_highest_sale,
      this.active_user_id.currency_id[0]
    )

    this.months_heighest_sale =
      sale_order_record["month_heighest_sale_amount_obj"];
    this.months_heighest_sale_amount_with_currency = await formatCurrency(
      this.months_heighest_sale,
      this.active_user_id.currency_id[0]
    )
    this.month_total_sale = sale_order_record["month_total_sale_obj"];

    if (
      Number(`${currenthour}.${current_minute}`) >= 5 &&
      Number(`${currenthour}.${current_minute}`) < 12
    ) {
      this.wish = "Good Morning";
    } else if (
      Number(`${currenthour}.${current_minute}`) >= 12 &&
      Number(`${currenthour}.${current_minute}`) < 17
    ) {
      this.wish = "Good Afternoon";
    } else if (
      Number(`${currenthour}.${current_minute}`) >= 17 &&
      Number(`${currenthour}.${current_minute}`) < 19
    ) {
      this.wish = "Good Evening";
    } else {
      this.wish = "Good Night";
    }
  }

  async monthlySaleRecords() {
    const monthlySaleRecords = await this.orm.call(
      "sale.order",
      "monthly_Sale_Order_Record",
      [[]],
    );
  }

  async onchangeStartDate() {
    this.top_sale_orders();
    await this.topProducts();
    await this.productAnalysis();
    this.topCustomerByRevenue();
    await this.customerAnalysisByRevenue();
    await this.saleOrderPendingDeliveries();
  }

  async onchangeEndDate(){
    this.top_sale_orders();
    await this.topProducts();
    await this.productAnalysis();
    this.topCustomerByRevenue();
    await this.customerAnalysisByRevenue();
    await this.saleOrderPendingDeliveries();
  }

  nf_set_start_end_date(){
    let date = new Date();
    let monthstartdate = new Date(date.getFullYear(),date.getMonth(),1);
    this.state.start_date = monthstartdate.toLocaleDateString("en-CA", {
        timeZone: this.state.user.tz,
    })
    this.state.end_date = new Date().toISOString().split("T")[0]
  }

  async get_sales_data_from_model(){
    return await this.orm.call(
          "sale.order",
          "nf_get_sales_data",
          [
              this.state.start_date,
              this.state.end_date,
              this.state.sales_chart,
          ]
      );
  }
  
  async onChangeSalesDetails(ev) {
    const sales_data = await this.get_sales_data_from_model();
    config4.series[0].data = [];
    config4.xaxis.categories = [];
    if(this.state.sales_chart == "today"){
      config4.plotOptions.bar.columnWidth = "150px";
      await sales_data.sales_record.forEach((ele) => {
          config4.series[0].data.push(ele.orderTotal);
          config4.xaxis.categories.push(`${ele.time[0]}-${ele.time[1]}`);
        });

      document.getElementById("nf-sale-monthly-record-chart").innerHTML = "";
      var InvoiceOrderChart = new ApexCharts(
          document.getElementById("nf-sale-monthly-record-chart"),
          config4
      );
      InvoiceOrderChart.render();
    }
    else if (this.state.sales_chart === 'month'){
        await sales_data.sales_record.forEach((ele) => {
            config4.series[0].data.push(ele.Amount);
            config4.xaxis.categories.push(ele.day);
        });

        document.getElementById("nf-sale-monthly-record-chart").innerHTML = "";
        var InvoiceOrderChart = new ApexCharts(
            document.getElementById("nf-sale-monthly-record-chart"),
            config4
        );
        InvoiceOrderChart.render();

    }else if (this.state.sales_chart === 'year'){
      config4.plotOptions.bar.columnWidth = "100px";
        await sales_data.sales_record.forEach((ele) => {
            config4.series[0].data.push(ele.Amount);
            config4.xaxis.categories.push(ele.month);
        });

        document.getElementById("nf-sale-monthly-record-chart").innerHTML = "";
        var InvoiceOrderChart = new ApexCharts(
            document.getElementById("nf-sale-monthly-record-chart"),
            config4
        );
        InvoiceOrderChart.render();
    }
  }

  async top_sale_orders() {
    const sale_orders = await this.orm.call(
      "sale.order",
      "top_Sale_Order_Record",
      [[],this.state.start_date,this.state.end_date],
    );
    this.state.top_sale_order_record = sale_orders["sale_order_object"];
    this.state.invoice_due_record = sale_orders["invoice_due_obj"];
    this.state.running_sale_order_record = sale_orders["running_sale_order_obj"];
  }

  async topProducts(){
    const top_products_record = await this.orm.call(
      "sale.order",
      "top_Selling_Product",
      [[],this.state.start_date,this.state.end_date],
    );
    this.state.top_selling_products = top_products_record["top_product_obj"];
    return this.state.top_selling_products;
  }

  async productAnalysis(){
    const top_products_record = await this.topProducts();
    const totalQty = top_products_record.reduce(
        (sum, item) => sum + item.sale_qty,
        0
    );

    const labels = [];
    const series = [];
    const colors = [];

    top_products_record.forEach((product, i) => {
        labels.push(product.product_name);
        const percentage = totalQty
            ? (product.sale_qty / totalQty) * 100
            : 0;

        series.push(Number(percentage.toFixed(2)));
        const hue = (i * 360) / top_products_record.length;
        colors.push(`hsl(${hue}, 70%, 55%)`);
    });

    if (!this.productChart) {
        sellingproductbyquantity.labels = labels;
        sellingproductbyquantity.series = series;
        sellingproductbyquantity.colors = colors;

        this.productChart = new ApexCharts(
            document.getElementById("nf-sale-product-by-qty-record-chart"),
            sellingproductbyquantity
        );

        await this.productChart.render();

    } else {
        if (!labels.length || !series.length) {
            await this.productChart.updateOptions({
                labels: ["No Data"],
                colors: ["#d3d3d3"],
            });

            await this.productChart.updateSeries([1]);

            return;
        }

        await this.productChart.updateOptions({
            labels: labels,
            colors: colors,
        });

        await this.productChart.updateSeries(series);
        }

  }

  async topCustomerByRevenue(){
    const topCustomersByRevenue = await this.orm.call(
      "sale.order",
      "top_customer_by_revenue",
      [[],this.state.start_date,this.state.end_date],
    );

    this.state.top_customer_by_revenue = topCustomersByRevenue["top_customer_record"];
    return topCustomersByRevenue["top_customer_record"]
  }
  display_amount_with_currency(amount){
    return formatCurrency(
        amount,
        this.active_user_id.currency_id[0]
    );
  }
  async customerAnalysisByRevenue(){
    const topCustomersByRevenue = await this.topCustomerByRevenue();
    
    const totalamount = topCustomersByRevenue.reduce(
        (sum, item) => sum + item.amount,
        0
    );
    
    const labels = [];
    const series = [];
    const colors = [];

    topCustomersByRevenue.forEach((customer, i) => {
        labels.push(customer.customer_name);
        const percentage = totalamount
            ? (customer.amount / totalamount) * 100
            : 0;

        series.push(Number(percentage.toFixed(2)));
        const hue = (i * 360) / topCustomersByRevenue.length;
        colors.push(`hsl(${hue}, 70%, 55%)`);
    })

    
    if (!this.customerRevenue) {
        topCustomerRevenueChart.labels = labels;
        topCustomerRevenueChart.series = series;
        topCustomerRevenueChart.colors = colors;

        this.customerRevenue = new ApexCharts(
            document.getElementById("nf-premium-customer-chart"),
            topCustomerRevenueChart
        );

        await this.customerRevenue.render();
        
      } else {
        if (!labels.length || !series.length) {
            await this.customerRevenue.updateOptions({
                labels: ["No Data"],
                colors: ["#d3d3d3"],
            });

            await this.customerRevenue.updateSeries([1]);

            return;
        }
        
          await this.customerRevenue.updateOptions({
              labels: labels,
              colors: colors,
          });
  
          await this.customerRevenue.updateSeries(series);
    }
  }

  async saleOrderPendingDeliveries(){
    const pendingDeliveries = await this.orm.call(
      "sale.order",
      "pending_sale_orders",
      [[],this.state.start_date,this.state.end_date],
    );

    this.state.pending_delivery_orders = pendingDeliveries["pending_delivery_order_obj"];
  }
}

registry
  .category("actions")
  .add("sale_management_dashboard", SaleManagement, { force: true });