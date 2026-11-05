# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale A4 Size Receipt",
    "summary": """ 
        Point Of Sale A4 Size Receipt point of sale a4 size receipt print point of sale a4 size receipt a4 size a4 size receipt print point of sale a4 size receipt pos a4 size receipt size receipt arabic a4 size receipt a4 size receipt in arabic arabic pos receipt arabic point of sale receipt qrcode invoice pos invoice with qr code change invoice desing change invoice looks pos receipt in a4 size invoice in a4 size pos receipt a4 a4 receipt  
        odoo pos a4 receipt pos a4 invoice point of sale a4 receipt odoo receipt printing pos invoice receipt qr code receipt tlv base64 qr ksa pos receipt saudi arabia qr code arabic pos receipt pos receipt template offline pos receipt odoo pos qr code a4 receipt printing invoice style pos receipt
        """,
    "author": "NextFlowIT",
    "license": "OPL-1",
    "description": """ 
        This Module is Use to print Point of sale Receipt in a4 size paper. This module is use to print receipt like an invoice, 
        Print professional A4-size receipts from Odoo Point of Sale with invoice-style layout, QR Code, TLV Base64 (KSA), Arabic labels, offline POS support, and full compatibility with the standard Odoo POS.
        """,
    # "post_init_hook": "post_init_hook",
    "category": "Point of sale",
    "website": "",
    "depends": ["point_of_sale"],
    "version": "0.0.1",
    "data": [
        "views/a4_receipt_config.xml",
        "views/res_config_setting_inherited_view.xml",
        "views/a4receipt_template.xml",
        
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_receipt_a4_size/static/src/override/FeedBackScreen.xml",
            "nf_pos_receipt_a4_size/static/src/override/FeedBackScreen.js",
            "nf_pos_receipt_a4_size/static/src/apps/NfPrintPopup.js",
            "nf_pos_receipt_a4_size/static/src/apps/NfPrintPopup.xml",
            # "nf_pos_receipt_a4_size/static/src/override/ReceiptScreen.js",
        ],
    },
    "images": [
        "static/description/background.gif",
    ],
    "price": 22.42,
    "installable": True,
    "application": True,
    "auto_install": False,
    "currency": "EUR",
}
