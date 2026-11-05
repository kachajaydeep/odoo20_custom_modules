# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': "Custom Font Family",
    'summary': """odoo google font family google fonts odoo odoo font customization odoo typography odoo ui customization odoo branding module custom fonts odoo odoo theme customization odoo interface font change google font integration odoo predefined fonts odoo sales font point of sale font odoo pos font corporate branding odoo responsive font module odoo frontend customization odoo user interface customization odoo 19 google fonts odoo apps typography module""",
    'post_init_hook': 'post_init_hook',
    'description': """Google Font Family module for Odoo allows you to customize the font family across your Odoo interface using predefined fonts or Google Fonts. Enhance branding, improve user experience, and apply consistent typography across Sales, Point of Sale, and other supported Odoo modules without any coding.""",
    'author': 'NextFlowIT',
    'license': "OPL-1",
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'nextflow.in',
    'version': '20.0.1',
    'data': [
        'views/res_config_settings.xml',
        'views/bootstrap_fonts.xml',
    ],
    "images": ["static/description/background.gif"],
    'application': True,
    'installable': True,
    'auto_install': False,
    "price": 79.99,
    "currency": "USD"
}
