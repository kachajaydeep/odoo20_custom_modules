# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Sale order boost',
    'summary': '''  Direct Line Add in Sale Order direct ine add in sale order quick add line in sale order import exls file in sale order line sale order line quick add product quick add quantity product qty matrix product matrix update product configuration popup update quick copy line from excel sale order speed boost  sale order line eacy boost sale order line multi vairiant add variant table view sale order with multi variant varinat from excel sheet ''',
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'description': """    """,
    'category': "Sale",
    'website': 'nextflow.in',
    'depends': ['sale', 'sale_management'],
    'version': '20.0.1',
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'nf_boost_sale_order/static/src/**/*',
        ],
    },
    "images": ["static/description/background.gif", ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': False,
    "price": 10.99,
    "currency": "EUR"
}
