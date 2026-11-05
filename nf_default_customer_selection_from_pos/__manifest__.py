# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': "Default Customer Selection From Point of Sale",
    'summary': """
        Default Customer pos default employee pos default partner pos default cashier pos cashier odoo default customer pos default customer point of sale default customer odoo pos customer selection automatic customer selection odoo retail module odoo point of sale customization pos customer automation default partner in pos odoo customer 
    """,
    # 'post_init_hook': 'post_init_hook',
    'description': """
        Automatically assign a default customer to every new Odoo Point of Sale order. Configure a default customer once using the POS configuration to speed up checkout, reduce manual customer selection, and improve billing efficiency.
    """,
    'data': [
        'views/res_config_settings_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_default_customer_selection_from_pos/static/src/overrides/pos_order.js',
        ],
    },
    'author': 'NextFlowIT',
    'license': "OPL-1",
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'https://www.nextflow.in',
    'version': '20.0.1',
    'depends': ['point_of_sale'],
    'images': ["static/description/background.gif"],
    'application': True,
    'installable': True,
    'auto_install': False,
    'price': 00.00,
    'currency': "USD"
}