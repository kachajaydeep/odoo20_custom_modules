# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.
{
    "name": "Analytic Account For Point Of Sale",
    'summary': """odoo pos analytic accounting point of sale accounting odoo configuration developer mode odoo pos settings analytic account assignment pos orders order lines accounting pos sessions financial tracking in odoo odoo backend orders accounting visibility profitability analysis odoo erp pos module analytic accounting for point of sale analytic account for point of sale point of sale analytic account point of sale analytic accounting""",
    'post_init_hook': 'post_init_hook',
    'description': """Learn how Analytic Accounting works in Odoo Point of Sale with step-by-step configuration, order processing, and session management. Understand analytic account assignment in POS orders and order lines, and how enabling or disabling the feature impacts financial tracking and reporting.""",
    "version":"20.0.1",
    "data":[
        'views/res_config_settings_inherited_view.xml',
        'views/pos_orderline.xml',
        'views/pos_session_view.xml',
    ],
    'assets':{
        'point_of_sale._assets_pos': [
            'nf_pos_analytic_account/static/src/overrides/pos_store/pos_store.js',
            'nf_pos_analytic_account/static/src/overrides/pos_order_line/pos_order_line.js',
        ],
    },
    'author': 'NextFlowIT',
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'https://www.nextflow.in',
    "depends":['point_of_sale','account'],
    "images": ["static/description/background.gif"],
    "license":'OPL-1',
    'application': False,
    'installable': True,
    'auto_install': False,
}
