# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Create Sale Order From Point of sale',
    'summary': ''' create sale order from pos generate so so_from_pos saleorder pos create sale order pos creation pos create so from po sale order pos order label point of sale order label order lable pos lable receipt order  cart label pos order section section pos section sale from pos pos to sale create so from pos sale order creation ''',
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'description': """ This App is use to create sale order form pos, This app add functionality in you system to genereate sale order from pos """,
    'post_init_hook': 'post_init_hook',
    'category': "Point of sale",
    'website': '',
    'depends': ['point_of_sale', 'sale_management'],
    'version': '18.0.0.0.1',
    'data': [
        'data/data.xml',
        'views/nf_config_pos.xml',
    ],
    'assets': {
       'point_of_sale._assets_pos': [
            'nf_pos_create_saleorder/static/src/app/buttons/*',
            'nf_pos_create_saleorder/static/src/app/popups/*',

        ],
    },
    "images": ["static/description/background.gif", ],
    "price": 25,
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR"
}
