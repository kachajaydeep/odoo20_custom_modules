# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 


{
    "name" : "Product Brand",
    "summary" : """
        odoo product brand brand management odoo odoo brand module odoo product brand management brand in sale order odoo brand in invoice odoo odoo product variant brand odoo brand assignment wizard product brand management odoo odoo sales brand management odoo brand reporting odoo product brand brand management odoo odoo brand module odoo product brand management brand in sale order odoo brand in invoice odoo odoo product variant brand odoo brand assignment wizard product brand management odoo odoo sales brand management odoo brand reporting odoo product brand module product brand management odoo odoo brand management system odoo product brand app odoo brand for products odoo brand for product variants brand in sale order odoo brand in invoice odoo brand in sale order line brand in invoice line brand in reports brand in sale order report brand in invoice report product brand configuration brand assignment wizard bulk brand assign odoo product brand management erp product brand customization sales brand management product catalog brand management brand module for sales brand tracking system Product Brand Product Brand Management Brand Product odoo product brand
    """,
    'post_init_hook': 'post_init_hook',
    "description" : """
        Manage product brands in Odoo with brand assignment for products and variants. Display brands in sales orders, invoices, and reports with bulk brand assignment wizard and advanced brand management.
            """,
    "data" : [
        'security/ir.access.csv',
        'wizard/nf_assign_brand_wizard_view.xml',
        'report/nf_sale_order_report.xml',
        'report/nf_sale_report_view.xml',
        'report/nf_invoice_report.xml',
        'wizard/nf_res_config_settings.xml',
        'views/nf_product_brand_view.xml',
        'views/nf_product_product_view.xml',
        'views/nf_product_template_view.xml',
        'views/nf_sale_order_view.xml',
        'views/nf_account_move_view.xml',
        'views/nf_menuitem.xml',
    ],
    "author": 'NextFlowIT',
    "company": 'NextFlow Technology',
    "support": "nextflow@gmail.com",
    "website": 'https://www.nextflow.in',
    "depends" : ['sale_management', 'product', 'account'],
    "version": "20.0.1",
    "license": 'OPL-1',
    "images": ["static/description/background.gif"],
    "installable" : True,
    "application": True,
    "auto_install": False,
    "price": 15.00,
    "currency": "USD"
}