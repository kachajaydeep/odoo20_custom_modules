# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

{
    "name":"Pos Barcode Return/Exchange",
    "summary":"""
        odoo pos barcode return odoo pos exchange module odoo barcode return system odoo point of sale return odoo pos barcode scanning odoo retail return management odoo pos exchange workflow odoo pos refund barcode odoo pos customization odoo point of sale exchange odoo barcode refund module odoo retail pos return odoo pos management odoo apps pos return nextflow technology odoo module pos barcode return exchange  pos exchange pos return pos barcode POS Barcode Pos Barcode Return Exchange pos return  pos exchange product barcode
    """,
    "post_init_hook": 'post_init_hook',
    "description":"""
        Process barcode-based product returns and exchanges directly in Odoo Point of Sale. Improve return management, barcode scanning, and customer service efficiency in Odoo.
    """,
    "data": [],
    "assets": {
        'point_of_sale._assets_pos': [
            "nf_pos_barcode_return_exchange/static/src/apps/popups/return_order_popup.js",
            "nf_pos_barcode_return_exchange/static/src/apps/popups/return_order_popup.xml",
            "nf_pos_barcode_return_exchange/static/src/apps/popups/return_order_popup.scss",
            "nf_pos_barcode_return_exchange/static/src/overrides/components/product_screen.js",
        ],
    },
    "images": ["static/description/background.gif"],
    "support": "nextflow@gmail.com",
    "author": 'NextFlowIT',
    "company": 'NextFlow Technology',
    "maintainer": 'NextFlow Technology',
    "website": 'https://www.nextflow.in',
    "version":"20.0.1",
    "depends": ['nf_pos_receipt_barcode'],
    "license": 'OPL-1',
    "application": True,
    "installable": True,
    "auto_install": False,
    "price": 45.0,
    "currency": "USD"
} 