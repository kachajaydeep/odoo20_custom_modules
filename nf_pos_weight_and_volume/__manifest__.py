# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': "Point of Sale Weight and Volume",
    'summary': """
        odoo point of sale pos order list pos order line weight and volume pos weight pos volume product weight product volume receipt weight receipt volume retail pos weight volume Weight and Volume pos weight and volume weight pos volume pos odoo pos weight odoo pos volume pos product weight pos product volume point of sale weight point of sale volume odoo receipt weight odoo receipt volume pos order line weight pos order line volume odoo retail odoo supermarket grocery pos warehouse weight  package volume
    """,
    # 'post_init_hook': 'post_init_hook',
    'description': """
        Manage product weight and volume directly in Odoo Point of Sale. Display weight and volume on POS order lines and customer receipts with configurable settings for a faster and more informative checkout process.
    """,
    'data': [
        'views/nf_pos_order_view.xml',
        'views/res_config_settings_view.xml',
        'views/pos_order_receipt_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_pos_weight_and_volume/static/src/overrides/pos_store/pos_store.js',
            'nf_pos_weight_and_volume/static/src/overrides/order_display/order_display.js',
            'nf_pos_weight_and_volume/static/src/overrides/order_display/order_display.xml',
            # 'nf_pos_weight_and_volume/static/src/overrides/order_receipt/order_receipt.js',
            # 'nf_pos_weight_and_volume/static/src/overrides/order_receipt/order_receipt.xml',
            'nf_pos_weight_and_volume/static/src/overrides/orderline/orderline.xml',
        ],
    },
    'author': 'NextFlowIT',
    'license': "OPL-1",
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'nextflow.in',
    'version': '20.0.1',
    'depends': ['point_of_sale'],
    'images': ["static/description/background.gif"],
    'application': True,
    'installable': True,
    'auto_install': False,
    'price': 15.00,
    'currency': "USD"
}