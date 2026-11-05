# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

{
    'name' : "Product Sale Report",
    'summary' : """
        odoo product sale report odoo product sales report odoo sales report pos product report odoo pos report sales order report product wise sales report category wise sales report odoo reporting module odoo sales analytics pos sales analytics odoo product analysis odoo retail reporting sales performance report odoo business report odoo product report odoo sales dashboard point of sale reportingodoo reporting odoo apps odoo odoo 19 odoo 18 odoo 17 product sale report point of sale report sales analytics pos analytics retail reporting business analytics inventory report odoo erp product sales analysis product pos report pos stock report sale stock report sale inventory report pos inventory report point of sale product report product inventory product stock on hand stock report
    """,
    'post_init_hook': "post_init_hook",
    'description' : """
        Generate detailed Product Sale Reports in Odoo using Sales Orders and Point of Sale. Filter by date, product category, and report type (Sales, POS, or Both). Download product-wise sales reports for better business analysis.
    """,
    'data' : [
        "security/ir.access.csv",
        "reports/nf_product_report_view.xml",
        "wizard/nf_product_sale_report_view.xml",
        "views/nf_menuitem.xml",     
        ],
    'version': "20.0.1",
    'author': "NextFlowIT",
    'company': "NextFlow Technology",
    'maintainer': "NextFlow Technology",
    'website': "https://nextflow.in/",    
    'depends' : ["sale", "point_of_sale", "stock"],
    'images': ["static/description/background.gif"],
    'license': "OPL-1",
    'installable': True,
    'auto_install': False,
    'application': True,
    "price": 12.00,
    "currency": "USD"
}