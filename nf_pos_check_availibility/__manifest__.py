# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Pos Stock status',
    'summary': ' pos stock check availibility stock notificaiton pos stock management manage stock in pos display stock  pos stock check availibility stock notificaiton pos stock management manage stock in pos display stock point of Sale Check Stock Availability on hand stock onhand stock pos stock stock available point of sale stock check pos stock check stock status pos stock status point of sale stock status check stock in pos Odoo POS Stock Status Odoo Point of Sale POS inventory Odoo inventory stock availability POS stock availability product stock real-time stock multi-location inventory Odoo POS inventory POS order search POS refund Odoo refund management retail inventory inventory management POS stock check Odoo retail Point of Sale inventory ',
    'post_init_hook': 'post_init_hook',
    'description': """ POS Stock Status for Odoo lets POS users check real-time product stock across locations, search orders quickly, and streamline refund management. """,
    'data': [
        'views/res_config_settings.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            "nf_pos_check_availibility/static/src/js/stock_button.js",
            "nf_pos_check_availibility/static/src/js/models.js",
            "nf_pos_check_availibility/static/src/js/pos_store.js",
            "nf_pos_check_availibility/static/src/xml/stock_button.xml",
            "nf_pos_check_availibility/static/src/scss/pos.scss"
        ],
    },
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'category': "Point of sale",
    'website': 'nextflow.in',
    'depends': ['point_of_sale','stock'],
    'version': '20.0.1',
    "images": ["static/description/background.gif", ],
    "price": 30.30,
    'live_test_ur': 'https://youtu.be/obh1aRchSlo',
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR"
}