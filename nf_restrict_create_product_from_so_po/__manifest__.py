# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

{
    'name': 'Restrict Create Product From So Po',
    'summary': """ 
        sale create purchase create  so po restrict create product from so po odoo product creation restriction restrict product creation in sales order restrict product creation in purchase order odoo sales order restriction odoo purchase order restriction prevent product creation from so prevent product creation from po odoo product management product catalog controlodoo inventory management sales order product restriction purchase order product restriction odoo user access control product master data control odoo business process control odoo sales customization odoo purchase customization product creation validation nextflow technology odoo module
        restrict create product disable create product button prevent product creation from sale order prevent product creation from purchase order restrict product creation odoo sale order restriction purchase order restriction product catalog control master data governance data integrity odoo clean product list restrict create and edit in product fiel
    """,
    'post_init_hook': 'post_init_hook',
    'description': """  
        Restrict users from creating new products directly from Sales Orders and Purchase Orders in Odoo. Improve data control, prevent unauthorized product creation, and maintain a clean and standardized product catalog across your business.
        restrict create product disable create product button prevent product creation from sale order prevent product creation from purchase order restrict product creation odoo sale order restriction purchase order restriction product catalog control master data governance data integrity odoo clean product list restrict create and edit in product fiel 
    """,
    "version":"20.0.1",
    'category': 'Extra Tools',
    'author': 'NextFlowIT',
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'nextflow.in',
    "depends":['sale_management','purchase'],
    "data":[
        'security/product_creation_access_groups.xml',
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
    ],
    'images': ['static/description/background.gif'],
    'license': "OPL-1",
    'installable': True,
    'auto_install': False,
    'application': False,
    "price": 5.00,
    "currency": "USD"
}
