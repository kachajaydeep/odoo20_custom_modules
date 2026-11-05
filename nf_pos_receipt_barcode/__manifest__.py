# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

{
    "name":"Pos Receipt Barcode",
    "summary":"""
        odoo pos receipt barcode odoo barcode receipt module odoo point of sale barcode receipt odoo pos order barcode odoo pos receipt customization odoo barcode scanning pos odoo retail receipt barcode odoo pos order tracking odoo pos barcode module odoo point of sale customization odoo receipt scanner odoo pos management odoo apps pos barcode odoo retail pos solution nextflow technology odoo module pos order receipt pos order receipt barcode pos barcode
    """,
    # "post_init_hook": 'post_init_hook',
    "description":"""
        Add barcode support to POS order receipts in Odoo Point of Sale for faster order tracking, barcode scanning, returns, and receipt management. Improve POS efficiency and customer service in Odoo.
    """,
    "data": [
        "data/nf_barcode_pattern.xml",
        "views/res_config_settings.xml",
        "views/pos_order_view.xml",
        "receipt/pos_order_receipt.xml",
    ],
    'assets': {},
    "images": ["static/description/background.gif"],
    "support": "nextflow@gmail.com",
    "author": 'NextFlowIT',
    "company": 'NextFlow Technology',
    "maintainer": 'NextFlow Technology',
    "website": 'https://www.nextflow.in',
    "version":"20.0.1",
    "depends": ['point_of_sale'],
    "license": 'OPL-1',
    "application": True,
    "installable": True,
    "auto_install": False,
    "price": 13.0,
    "currency": "USD"
} 