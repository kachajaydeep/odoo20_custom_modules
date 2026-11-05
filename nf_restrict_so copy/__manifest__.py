# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Create SO Restriction',
    'summary': """ 
        sales restrict create so restriction odoo sales order restriction restrict sales order creation odoo stock validation insufficient stock restriction prevent overselling odoo sales order stock check odoo inventory control stock availability validation odoo sales management negative stock restriction product stock validation sales order restriction module inventory management odoo nextflow technology odoo module
        create so restriction create_so_restriction sale restriction out of stock restriction out out of stock so restriction stock authentication so authentication sale order authentication restrict so 
    """,
    'author': 'NextFlowIT',
    "license": "OPL-1",
    # 'post_init_hook': 'post_init_hook',
    'description': """ 
        Restrict Sales Order creation in Odoo when product stock is insufficient. Prevent users from creating sales orders beyond available stock, avoid overselling, and improve inventory control with automated stock validation.
        Restrict to create so if then stock is low. 
        If on hand stock is low and try to create so more than on hand qty one warning is raise for low stock. 
        Prevent Sales Orders when product stock is insufficient. Get stock warnings and restrict users from selling quantities greater than available on-hand stock in Odoo.
        """,
    'category': "sale",
    'website': 'nextflow.in',
    'depends': ['sale_management', 'stock'],
    'version': '0.0.1',
    "data": [ 'security/inventory_security.xml' ],  
    "images": ["static/description/background.gif", ],
    "price": 18.42,
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR"
}
