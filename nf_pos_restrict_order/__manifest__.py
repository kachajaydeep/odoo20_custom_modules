# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Restrict Out Of Stock",
    "summary": """ 
        pos restrict out of stock product order creation designed to streamline your inventory management processes and enhance customer satisfaction inventory management for pos out of stock prevention order creation restriction stock control inventory optimization streamlined operations real time inventory monitor pos order creation restriction pos stock restriction pos stock restrict pos order restriction pos order restriction sale order restriction restrict pos order restrict odoo point of sale odoo pos out of stock restriction odoo out of stock pos odoo pos stock management restrict out of stock products odoo odoo pos inventory control prevent out of stock sales odoo point of sale out of stock prevention odoo pos inventory management pos out of stock management 
        pos restrict out of stock pos stock restriction odoo pos inventory control pos prevent overselling pos stock validation out of stock restriction odoo point of sale stock check pos product availability pos inventory management odoo retail stock control odoo pos module inventory restriction real-time stock validation pos stock management    
    """,
    "author": "NextFlowIT",
    "license": "OPL-1",
    "description": """ 
        POS Restrict Out of Stock Product Order Creation designed to streamline your inventory management processes and enhance customer satisfaction. 
        Prevent out-of-stock product sales in Odoo Point of Sale with real-time stock validation. Automatically restrict unavailable products, prevent overselling, improve inventory accuracy, and streamline retail operations.    
    """,
    "post_init_hook": "post_init_hook",
    "category": "Point of sale",
    "website": "",
    "depends": ["point_of_sale", "nf_pos_stock_info"],
    "version": "20.0.1",
    "data": ["views/pos_res_settings.xml"],
    "assets": {
        "point_of_sale._assets_pos": ["nf_pos_restrict_order/static/src/overrides/**/*"]
    },
    "images": [
        "static/description/background.gif",
    ],
    "price": 12.00,
    "installable": True,
    "application": True,
    "currency": "EUR",
}