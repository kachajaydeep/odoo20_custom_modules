# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Create SO Restriction',
    'summary': """ create so restriction create_so_restriction sale restriction out of stock restriction out out of stock so restriction stock authentication so authentication sale order authentication restrict so """,
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'post_init_hook': 'post_init_hook',
    'description': """ Restrict to create so if then stock is low. 
        If on hand stock is low and try to create so more than on hand qty one warning is raise for low stock. """,
    'category': "sale",
    'website': 'nextflow.in',
    'depends': ['sale_management', 'stock'],
    'version': '20.0.2',
    "data": [ 'security/inventory_security.xml' ],
    "images": ["static/description/background.gif", ],
    "price": 18.42,
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR"
}
