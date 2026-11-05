# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

{
    "name": "Cashier Discount Limit From Pos",
    'summary': """odoo pos discount limit pos restriction cashier discount control employee discount control pos price security point of sale product discount category discount odoo 19 pos pos validation discount manager sales control pos fixed discount pos percentage discount discount limit product discount pos product category limit category  pos customer discount limit pos discount pos employee discount limit """,
    'post_init_hook': 'post_init_hook',
    'description': """Restrict POS discounts by product or category. Set fixed or percentage limits for employees prevent unauthorized price drops, and ensure real-time POS validation.""",
    "version":"20.0.1",
    "data":[
        'views/product_inherit_view.xml',
        'views/res_config_settings_inherit_view.xml',
        'views/product_category_inherit_view.xml',
    ],
    'author': 'NextFlowIT',
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'https://www.nextflow.in',
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_discount_limit_from_pos/static/src/overrides/order_summary/order_summary.js',
            'nf_discount_limit_from_pos/static/src/overrides/pos_store/pos_store.js',
            'nf_discount_limit_from_pos/static/src/overrides/pos_order/pos_order.js',
        ],
    },
    'depends':["point_of_sale"],
    "images": ["static/description/background.gif"],
    'license': "OPL-1",
    'application': False,
    'installable': True,
    'auto_install': False,
    "price": 35.50,
    "currency": "EUR"
}