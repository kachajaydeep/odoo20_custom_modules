# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

{
    "name":"Pos Orderline Pricelist",
    "summary":"""
        odoo pos orderline pricelist odoo pos line pricelist odoo pos product pricing odoo point of sale pricelist odoo pos pricing rules odoo pos discount management odoo pos promotional pricing odoo pricelist per order line odoo pos customer pricing odoo retail pricing management odoo pos price customization odoo point of sale pricing module odoo pos sales pricing odoo pricelist integration nextflow technology odoo module odoo pos dynamic pricing odoo pos advanced pricelist pos price list pos pricelist pos price discount pricelist pos price list pos pos discount discount pricelist pricelist discount pos orderline pos sale pos product price
    """,
    "post_init_hook": 'post_init_hook',
    "description":"""
        Apply different pricelists directly on individual POS order lines in Odoo Point of Sale. Manage product-specific pricing, discounts, promotions, and customer-based rates with flexible order line pricelists in Odoo.
    """,
    "data": [
        "views/pos_orderline_view.xml",
        "views/receipt.xml",
    ],
    "assets": {
        'point_of_sale._assets_pos': [
            "nf_pos_orderline_pricelist/static/src/overrides/models/pos_orderline.js",
            "nf_pos_orderline_pricelist/static/src/overrides/components/orderline.js",
            "nf_pos_orderline_pricelist/static/src/overrides/display/orderline_display.xml",
        ],
    },
    "author": 'NextFlowIT',
    "company": 'NextFlow Technology',
    "website": 'https://www.nextflow.in',
    "license":"OPL-1",
    "version":"20.0.1",
    "depends": ['point_of_sale'],
    "images": ["static/description/background.gif"],
    "application": True,
    "installable": True,
    'auto_install': False,
    "price": 60.00,
    "currency": "USD"
}