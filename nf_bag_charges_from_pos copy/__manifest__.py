# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': "Bag Charges From Point of Sale",
    'summary': """
        odoo pos bag charges odoo carry bag charge pos plastic bag charge odoo shopping bag fee pos bag billing odoo retail pos odoo pos automation odoo pos category odoo supermarket pos odoo grocery pos odoo point of sale extensions pos product bag charges point of sale bag charge pos charge pos products bag charges pos shopping bag charges
    """,
    'post_init_hook': 'post_init_hook',
    'description': """
        Automatically apply carry bag charges in Odoo Point of Sale using configurable bag charge settings and a dedicated Carry Bag Category. Improve billing accuracy, automate checkout, and comply with paid bag regulations.
    """,
    'data': [
        'views/res_config_settings_inherited_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_bag_charges_from_pos/static/src/apps/**/*',
            'nf_bag_charges_from_pos/static/src/overrides/**/*',
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
    'price': 8.60,
    'currency': "USD"
}