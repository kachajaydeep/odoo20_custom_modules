# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Order list",
    "summary": """ 
        point of sale order management pos order tracking order list software retail order management pos order processing point of sale order tracking system efficient order lists for pos retail order fulfillment order management solutions pos transaction tracking streamlined pos orders point of sale inventory management order processing software pos sales order system point of sale order workflow retail pos order history order list optimization pos order automation e-commerce pos order system in-store order list solutions pos order list point of sale order list list orders list order 
        odoo pos order list  point of sale order list sale order list point of sale order management odoo pos orders pos order tracking pos order history odoo reorder pos order pos order search point of sale order screen odoo retail management pos order details odoo pos customization order list in pos pos orderline management retail pos solution odoo point of sale app pos order monitoring odoo pos productivity responsive pos interface pos quick reorder odoo apps store odoo 18 pos module point of sale order history odoo retail pos enhancement order management system odoo pos sales tracking remove    
    """,
    "author": "NextFlowIT",
    "license": "OPL-1",
    "description": """ 
        Point of Sale Order List for Odoo helps users manage POS orders with real-time updates, advanced order tracking, quick search, detailed order information, customizable order screens, and one-click reorder functionality for improved efficiency.
    """,
    "category": "Point of sale",
    "website": "",
    "depends": ["point_of_sale"],
    "version": "20.0.1",
    "data": ["views/res_pos_config.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_order_list/static/src/apps/buttons/order_list_button/order_list_button.js",
            "nf_pos_order_list/static/src/apps/buttons/order_list_button/order_list_button.xml",
            "nf_pos_order_list/static/src/apps/popups/nf_order_lines/*",
            "nf_pos_order_list/static/src/screens/order_list/*",
            "nf_pos_order_list/static/src/apps/store/pos_store.js",
        ]
    },
    "images": [
        "static/description/background.gif",
    ],
    "post_init_hook": "post_init_hook",
    "price": 25.42,
    "installable": True,
    "application": True,
    "currency": "EUR",
}
