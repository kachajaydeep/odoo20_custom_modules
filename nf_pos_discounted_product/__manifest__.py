# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point of Sale Discounted Price",
    "summary": """
        Point of Sale Discounted Price pos Price show and actual price in pos show discount in pos price in pos pricelist price display pos order discounte discount per product base discount display line discount display in show price price discounte show price in receipt show price line price discounted pricelist detail pricelist price pos display price pos display pricelist pos display pos receipt pos discount pos discounted pricelist disocunt
        odoo pos discount odoo pos discounted price odoo pricelist receipt pos original price pos receipt discount odoo receipt discount point of sale pricelist odoo pos receipt customization odoo pos strikethrough price odoo pos line discount odoo thermal receipt discount odoo offline pos product discount prodcut dicounted pos order prodcut discount
    """,
    "post_init_hook": "post_init_hook",
    "description": """ 
        This module is help you to display product actual price and discounted price in pos Point of Sale Discounted Price show discount in pos.
        Display original price, discounted price, and line discounts in Odoo POS using Pricelists. Show strikethrough prices in the cart and receipt with full Offline Mode support.
    """,
    "data": [
        "views/nf_pos_config_view.xml",
        "views/receipt.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_discounted_product/static/src/overrides/orderline/*",
        ],
    },
    "author": "NextFlowIT",
    "license": "OPL-1",
    "images": [
        "static/description/background.gif",
    ],
    "category": "Point of sale",
    "website": "https://www.nextflow.in",
    "depends": ["point_of_sale"],
    "version": "20.0.1",
    "price": 30,
    "installable": True,
    "application": True,
    "auto_install": False,
    "currency": "EUR",
}