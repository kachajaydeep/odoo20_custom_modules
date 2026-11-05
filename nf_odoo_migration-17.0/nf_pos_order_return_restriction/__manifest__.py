# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Pos Order Return Restriction',
    'summary': ' point of sale restrict to create a refund after expire policy days restrict to create order restrict create order restrict create pos order restrict to create pos order refund restriction  refund pos order restriction refund order restriction restrict order restrict pos order ',
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'description': """ point of sale restrict to create a refund after expire policy days """,
    'category': "Point of sale",
    'website': '',
    'depends': ['point_of_sale'],
    'version': '0.0.1',
    'data': [
        'views/res_config_settings.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_pos_order_return_restriction/static/src/overrides/*',
        ],
    },
    "images": ["static/description/background.gif", ],
    "price": 45.30,
    'live_test_ur': 'https://youtu.be/obh1aRchSlo',
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR"
}
