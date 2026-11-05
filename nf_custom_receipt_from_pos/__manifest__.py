# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': "Custom Receipt From Point of Sale",
    'summary': """""",
    'post_init_hook': 'post_init_hook',
    'description': """""",
    'author': 'NextFlowIT',
    'license': "OPL-1",
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'nextflow.in',
    'version': '20.0.1',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.access.csv',
        'data/nf_custom_receipt_template_data.xml',
        'views/nf_pos_receipt_template_view.xml',
        'views/res_config_settings_inherited_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_custom_receipt_from_pos/static/src/app/**/*',
        ],
    },
    "images": ["static/description/background.gif"],
    'application': False,
    'installable': True,
    'auto_install': False,
    "price": 79.99,
    "currency": "USD"
}