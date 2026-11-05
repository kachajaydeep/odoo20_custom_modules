# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Dashboard | Dashboard",
    "summary": """ pos dashboard pos analysis pos bussiness pos machine pos total sale data pos prediction pos dashboard odoo odoo pos analytics pos business intelligence odoo odoo pos reporting module point of sale dashboard odoo total sales report odoo sales summary pos pos sale analysis odoo odoo sales performance dashboard daily sales report odoo pos real-time pos dashboard odoo odoo pos sales trend odoo pos for retail business pos system for small business odoo point of sale for restaurants odoo pos machine integration pos hardware setup odoo odoo pos with barcode scanner pos and inventory management odoo complete pos system odoo odoo pos data analysis pos sales forecasting odoo odoo pos prediction module sales trend prediction odoo predict future sales odoo pos ai in odoo pos odoo pos machine learning integration odoo pos insights with python odoo pos total sales data smart dashboard odoo pos  Odoo Dashboard, OneView Dashboard, One View Dashboard, CRM Dashboard, Pos Dashboard, Sale Dashboard, Sales Dashboard, Accounting Dashboard, Inventory Dashboard, Purchase Dashboard, Invoice Dashboard, HR Dashboard, All-in-One Dashboard, Smart Business Dashboard, Best Odoo Dashboard, Advanced Analytics Dashboard, Odoo Reports, Odoo Apps Dashboard, Beautiful Custom Dashboard, Predefined Dashboard, Create Dashboard, Modern Odoo Dashboard, Dashboard Studio, Dashboard Builder, Dashboard Designer, Odoo Visualization App, Dynamic Reporting Dashboard, Real-time KPI Dashboard, Graph Chart Table View, Multiple Dashboards, Powerful Odoo Dashboard, Business Intelligence Dashboard, KPI Dashboard for Odoo, OneView BI Dashboard, OneView Analytics, OneView Studio, AI Dashboard, All in One Dynamic Dashboard, All in One Dashboard, All in One Odoo best, ninja dashboard, ninja dashboard, Advance ninja, Advance ninja dashboard, Powerful Odoo Dashboard, Dynamic Reporting, Graph Chart Table View, Business Intelligence for Odoo ,Mobile-Friendly Dashboard, Visual Dashboard for Odoo, Drag-and-Drop Dashboard Odoo POS Dashboard Odoo Point of Sale Dashboard Odoo POS Reporting Odoo POS Analytics Odoo POS System Dashboard""",
    "author": "NextFlowIT",
    "license": "OPL-1",
    "description": """ The Odoo Point of Sale Dashboard gives you a real-time, interactive view of your retail or restaurant operations. It is designed to provide business owners, managers, and cashiers with instant insights into sales performance, inventory status, and customer activity.

        Key Highlights:

        Sales Overview – Track total sales, average order value, and top-selling products at a glance.

        Cash Flow Monitoring – View payment methods, daily cash-in/cash-out, and pending transactions.

        Product & Inventory Insights – Monitor best-performing products, stock availability, and low-stock alerts.

        Employee Performance – Evaluate cashier or sales agent activity and compare performance.

        Customer Trends – Analyze repeat customers, loyalty points, and buying patterns.

        Multi-Store View – Manage multiple POS locations and consolidate sales data in one dashboard.

        Real-Time Updates – All data is synced instantly with Odoo, ensuring accuracy and transparency.

        This dashboard not only improves decision-making but also helps businesses reduce losses, optimize stock, and boost overall efficiency by centralizing key POS metrics in one intuitive view.
    """,
    "post_init_hook": "post_init_hook",
    "category": "Point of sale",
    "website": "",
    "depends": ["point_of_sale", "spreadsheet"],
    "version": "20.0.1",
    "data": [
        "security/ir.access.csv",
        "data/data.xml",
        "views/nf_dashboard.xml",
    ],
    "assets": {
        "spreadsheet.o_spreadsheet": [
            "nf_pos_dashboard/static/src/js/ApexCharts.js",
            "nf_pos_dashboard/static/src/js/nf_pos_new_dashboard.js",
            "nf_pos_dashboard/static/src/xml/nf_pos_dashboard.xml",
        ],
        "web.assets_backend": [
            "nf_pos_dashboard/static/src/assets/dashboard_action_loader.js",
            "nf_pos_dashboard/static/src/scss/custom.scss",
            "nf_pos_dashboard/static/src/scss/nf_dashboard.scss",
        ],
    },
    "images": [
        "static/description/background.gif",
    ],
    "price": 52.30,
    "live_test_ur": "https://youtu.be/obh1aRchSlo",
    "installable": True,
    "application": True,
    "auto_install": False,
    "currency": "EUR",
}
