# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

{
    'name':"Hide Cost Sale Price",
    'version': '20.0.1',
    'depends' : ['account','sale_management','product','stock','purchase'],
    'data': [
        'securtity/hide_price.xml',
        'views/nf_account_move_view.xml',
        'views/nf_product_combo_view.xml',
        'views/nf_product_product_view.xml',
        'views/nf_product_supplieInfo.xml',
        'views/nf_product_template_view.xml',
        'views/nf_purchase_bill_line_match.xml',
        'views/nf_purchase_history_list.xml',
        'views/nf_purchase_order_view.xml',
        'views/nf_purchase_report.xml',
        'views/nf_sale_report.xml',
        'views/nf_sale_view.xml',
        # 'views/nf_stock_production_lot_view.xml',
        'views/nf_stock_location_view.xml',
        'views/nf_product_attribute.xml',
        'views/nf_payment_view.xml',
    ],
    'description':'Hide Cost Sale Price is a powerful Odoo module designed to enhance data security by restricting visibility of product cost and sale prices across Sales, Purchase, Invoice, Stock, Accounting, and Product modules. It allows administrators to control who can view sensitive pricing information, ensuring better confidentiality and business security within Odoo. This module is ideal for companies that want to protect margin details, maintain pricing privacy, and implement role-based access control for financial data across the entire ERP system.',
    'post_init_hook': 'post_init_hook',
    'summary':'''
        hide price hide cost  sale price cost product price hide show sale price hide purchase unit price hide stock hide price cost odoo hide cost price module odoo hide sale price module hide product cost odoo hide purchase price odoo odoo product cost security odoo sales price restriction module odoo inventory cost hide odoo stock cost price security odoo accounting cost hide odoo invoice cost hide module odoo product price visibility control odoo erp security module hide cost price from users odoo hide sale price from users odoo odoo multi level access price control odoo product cost protection odoo business security module odoo apps marketplace cost hide module
        Odoo sales discount Odoo total discount sale order Odoo discount percentage sale order Odoo show discount amount Odoo display discount in sales Odoo sales management discount Odoo sales order discount report Odoo sales discount summary Odoo sales order discount percentag Odoo discount amount calculatio Odoo order line discount aggregatio Odoo multi-currency discount support How to show total discount in Odoo sales orde Odoo module to calculate total discount amoun Display total discount and percentage in Odo Odoo sales order discount tracking modul Odoo app for discount analysis in sale Odoo sales manager discount visibilit Odoo module for discount reporting in sales Sales Managemen Discount Report Business Tool Sales Orders
        
        ''',
     
    'category': 'Sale',
    "license": "OPL-1",
    'author': 'NextFlowIT',
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'nextflow.in',
    "images": ["static/description/background.gif"],
    'application': True,
    'installable': True,
    'auto_install': False,
    "price": 9.00,
    "currency": "EUR"
}