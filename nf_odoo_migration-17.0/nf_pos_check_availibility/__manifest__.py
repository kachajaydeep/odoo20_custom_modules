# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Pos Stock status',
    'summary': ' ',
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'description': """  """,
    'category': "Point of sale",
    'website': '',
    'depends': ['point_of_sale'],
    'version': '0.0.1',
    'data': [
        'views/res_config_settings.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_pos_check_availibility/static/src/apps/buttons/*',
            'nf_pos_check_availibility/static/src/overrides/models/*'
        ],
    },
    "images": ["static/description/background.gif", ],
    "price": 30.30,
    'live_test_ur': 'https://youtu.be/obh1aRchSlo',
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR"
}
