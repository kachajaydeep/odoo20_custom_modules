# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Sale Dashboard | Dashboard',
    'summary': ' pos dashboard pos analysis pos bussiness pos machine pos total sale data pos prediction',
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'description': """ The detailed description and pos bussiness Analysis """,
    'category': "Sale",
    'website': '',
    'depends': ['sale'],
    'version': '0.0.1',
    'data': [
        # 'views/nf_dashboard.xml',
        # 'security/ir.model.access.csv',
        # 'data/data.xml'
        'views/sale_dashboard_view.xml',
        'views/sale_dashboard_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'nf_sale_dashboard/static/src/js/sale_dashboard.js',
            'nf_sale_dashboard/static/src/xml/sale_dashboard_template.xml',
            'nf_sale_dashboard/static/src/js/ApexCharts.js',
            # 'nf_sale_dashboard/static/src/js/nf_pos_new_dashboard.js',
            'nf_sale_dashboard/static/src/scss/nf_dashboard.scss',
            # 'nf_sale_dashboard/static/src/xml/nf_pos_dashboard.xml',
        ],
    },
    "images": ["static/description/background.gif", ],
    "price": 52.30,
    'live_test_ur': 'https://youtu.be/obh1aRchSlo',
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR"
}
