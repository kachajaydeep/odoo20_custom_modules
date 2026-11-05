# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

{
    "name":"Pos Product Image Preview",
    "summary":"""
        odoo pos product image odoo point of sale image module odoo pos image display odoo pos product display odoo retail pos customization odoo pos ui enhancement odoo product image support odoo point of sale customization odoo pos interface module odoo apps pos product image odoo pos usability improvement odoo pos development odoo retail management odoo product catalog display nextflow technology odoo module odoo pos image preview product image image preview pos product image odoo pos Image pos Product Image Product image preview
    """,
    'post_init_hook': 'post_init_hook',
    "description":"""
        Display product images directly in Odoo Point of Sale for faster product identification and improved cashier experience. Enhance POS usability and accuracy with product image support in Odoo.
    """,
    "data": [],
    "assets": {
        'point_of_sale._assets_pos': [
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css",
            'nf_pos_image_preview/static/src/app/popups/imagePopup/*',
            'nf_pos_image_preview/static/src/overrides/*',
        ],
    },
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
    "price": 5.0,
    "currency": "USD"
}