# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Pos Order Return Restriction',
    'summary': """point of sale restrict to create a refund after expire policy days restrict to create order restrict create order restrict create pos order restrict to create pos order refund restriction  refund pos order restriction refund order restriction restrict order restrict pos order pos refund restrict pos refund restriction pos order refund restrict pos order restriction refund restriction refund restrict point of sale order return restriction pos order refund restrict, refund policy odoo 18 pos pos return process pos order management return restrictions in odoo pos pos return policy pos order restrictions pos sales return odoo point of sale return return limit odoo pos pos return settings pos restriction rules odoo pos customization pos order return control point of sale return restrictions pos return time limit pos refund restrictions pos return permissions pos order adjustment odoo pos configuration pos order modification odoo pos return management
        odoo pos refund restriction odoo pos return restriction pos refund policy odoo pos return policy pos refund management odoo pos refunds odoo pos order return pos return management odoo point of sale refund odoo point of sale return pos refund limit expired refund restriction pos order search odoo pos order search pos reorder odoo retail refund management odoo retail return policy pos transaction management odoo pos module odoo apps
        """,
    'post_init_hook': 'post_init_hook',
    'description': """
        The Pos Order Return Restriction module enhances Odoo's Point of Sale (POS) by introducing strict return control policies. It prevents unauthorized refunds, reducing financial risks and fraud in retail operations. This module ensures that only authorized users can process order returns, maintaining a secure and controlled sales environment.
        Control Odoo POS refunds with configurable return periods. Automatically restrict expired refunds, quickly find orders, and streamline POS return management.
        """,
    'data': [
        'views/res_config_settings.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_pos_order_return_restriction/static/src/overrides/*'
        ],
    },
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'category': "Point of sale",
    'website': 'nextflow.in',
    'depends': ['point_of_sale'],
    'version': '20.0.1',
    "images": ["static/description/background.gif", ],
    'live_test_ur': 'https://youtu.be/obh1aRchSlo',
    'installable': True,
    'application': True,
    'auto_install': False,
    "price": 40.00,
    "currency": "EUR"
}
