# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.
{
    "name": "Sale Dashboard",
    "summary": """odoo sales dashboard sales analytics odoo dashboard module sales reporting top selling products top customers revenue kpi dashboard odoo real-time sales reports odoo sales charts pie chart dashboard donut chart odoo sales performance analysis odoo reporting tool business analytics odoo sales data visualization multi company dashboard odoo 19 sales module export sales reports advanced sales filters fully responsive layout top products recent delivery orders top customers""",
    "post_init_hook": "post_init_hook",
    "description": """Sales Dashboard module for Odoo provides real-time sales analytics with interactive charts, KPI cards, and advanced filtering. Track top-selling products, top customers, and revenue insights with downloadable reports in SVG, PNG, and CSV formats. Fully responsive and multi-company supported dashboard for smarter business decisions.""",
    "version": "20.0.1",
    "data": [
        "views/sale_order_dashboard_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "nf_sale_dashboard/static/src/js/ApexCharts.js",
            "nf_sale_dashboard/static/src/scss/sale_management_dashboard_custom.scss",
            "nf_sale_dashboard/static/src/scss/sale_management_dashboard.scss",
            "nf_sale_dashboard/static/src/js/sale_management_dashboard.js",
            "nf_sale_dashboard/static/src/xml/sale_management_dashboard.xml",
        ],
    },
    "author": "NextFlowIT",
    "company": "NextFlow Technology",
    "maintainer": "NextFlow Technology",
    "website": "https://www.nextflow.in",
    "depends": ["web", "sale_management", "stock", "spreadsheet"],
    "images": ["static/description/background.gif"],
    "license": "OPL-1",
    "application": False,
    "installable": True,
    "auto_install": False,
    "price": 35.00,
    "currency": "USD",
}
