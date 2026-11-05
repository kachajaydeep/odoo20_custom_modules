# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'All in one Sale Restriction || Pos Sale Restriction || Transfer restriction',
    'summary': """ point of sale restrict sale if stock is low or don't have enough stock all in one restriction Restrict Stock Transfer restrict stock transfer restrict internal transfer create so restriction out of stock restriction out out of stock so restriction stock authentication so authentication sale order authentication pos restrict low stock restrict create pos order out of stock restriction inventory restriction pos warehpuse quantity display warehpuse qty display stock in pos display stock point of sale display stock pos restriction so po restrict transfer restrict full restrict order restriction """,
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'post_init_hook': 'post_init_hook',
    'description': """ Restrict to create so if then stock is low. 
        If on hand stock is low and try to create so more than on hand qty one warning is raise for low stock. """,
    'category': "",
    'website': 'nextflow.in',
    'depends': ['sale_management', 'stock', 'nf_restrict_so', 'nf_restrict_transfer'],
    'version': '19.0.0.0.1',
    "images": ["static/description/background.gif", ],
    "price": 5.00,
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR"
}
