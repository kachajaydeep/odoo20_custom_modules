# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Restrict Sale",
    "summary": """ 
        point of sale restrict sale if stock is low or don't have enough stock, pos restrict low stock restrict create pos order out of stock restriction inventory restriction pos warehpuse quantity display warehpuse qty pos restrict sale order sale order restriction pos sale restriction  
        odoo pos restrict sale pos stock restriction point of sale stock validation odoo pos available quantity pos warehouse stock pos product quantity display prevent negative stock restrict pos order odoo pos inventory pos on hand quantity warehouse location stock odoo retail pos stock warning odoo point of sale inventory control stock management multi warehouse pos odoo pos apps retail management odoo module
        point of sale odoo stock pos stock pos stock restriction restrict pos sale prevent negative stock available quantity warehouse quantity stock warning inventory management retail software warehouse management pos stock pos inventory stock point of sale stock multi warehouse display stock display inventory  qty pos display stock pos inventory display on hand stock pos stock inventory
        """,
    "post_init_hook": "post_init_hook",
    "description": """ 
        This product is helps you to restict create pos order if you don't have enough stock in your warehouse. 
        Prevent selling out-of-stock products in Odoo POS with real-time warehouse stock display. Show available quantity on the POS product screen, restrict sales based on stock availability, display low stock warnings, and use the POS default warehouse location for accurate inventory management.
        """,
    "category": "Point of sale",
    "website": "nextflow.in",
    "depends": ["point_of_sale", "nf_pos_stock_info"],
    "version": "20.0.1",
    "author": "NextFlowIT",
    "license": "OPL-1",
    "data": [
        "views/pos_config.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_sale_restriction/static/src/overrides/product_screen/product_screen.js",
            "nf_pos_sale_restriction/static/src/overrides/models/store.js",
        ]
    },
    "images": ["static/description/background.gif"],
    "price": 30.00,
    "installable": True,
    "application": True,
    "auto_install": False,
    "currency": "EUR",
}
