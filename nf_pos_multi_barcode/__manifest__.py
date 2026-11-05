# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Multi Barcode",
    "description": """
        Point Of Sale Multi Barcode for Odoo allows you to assign multiple barcodes to a single product and scan any barcode in POS to quickly identify and add the product to an order. Improve barcode management and speed up your Odoo Point of Sale operations.
    """,
    'post_init_hook': 'post_init_hook',
    "summary": """ 
        odoo pos multi barcode point of sale multi barcode odoo multiple product barcode pos barcode scanner odoo pos barcode multiple barcode product odoo alternative product barcode odoo retail barcode pos product scanning odoo barcode management multi barcode odoo odoo point of sale barcode pos multi barcode pos barcode pos product barcode sale barcode purchase barcode invoice barcode bill barcode
        odoo pos multi barcode point of sale multi barcode odoo multiple barcode odoo pos barcode odoo barcode scanner multi barcode product alternative product barcode odoo retail barcode pos product scanning odoo barcode management odoo point of sale odoo pos customization odoo retail management barcode scanning in odoo odoo apps store
    """,
    "data": [
        'data/product_multi_barcode.xml',
        'views/res_config_settings_inherit.xml',
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_multi_barcode/static/src/override/product_product.js",
            "nf_pos_multi_barcode/static/src/override/product_screen.js",
        ]
    },
    "author": "NextFlowIT",
    "license": "OPL-1",
    "category": "Point of sale",
    "website": "https://www.nextflow.in",
    "depends": ["point_of_sale", "nf_multi_barcode"],
    "version": "20.0.1",
    "images": ["static/description/background.gif",],
    "price": 45.00,
    "installable": True,
    "application": True,
    "auto_install": False,
    "currency": "USD",
}
