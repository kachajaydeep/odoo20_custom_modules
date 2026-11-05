# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point of sale Toppings",
    "summary": """pos toppings pos add ons pos system upgrades retail pos features pos integrations pos analytics tools pos inventory management pos billing software business pos solutions pos enhancements pos modifier product modification product modify pizza toppings""",
    "post_init_hook": "post_init_hook",
    "description": """
Enhance your POS system with powerful POS toppings including inventory management, analytics, billing tools, customer management, and integrations to streamline your business operations.
    """,
    "author": "NextFlowIT",
    "license": "OPL-1",
    "company": "NextFlow Technology",
    "maintainer": "NextFlow Technology",
    "website": "https://www.nextflow.in",
    "version": "20.0.1",
    "depends": ["point_of_sale", "pos_restaurant"],
    "data": [
        "security/ir.access.csv",
        "views/product_product_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_toppings/static/src/apps/toppings_popup/toppings_popup.js",
            "nf_pos_toppings/static/src/apps/toppings_popup/toppings_popup.xml",
            "nf_pos_toppings/static/src/apps/toppings_popup/toppings_popup.scss",
            "nf_pos_toppings/static/src/overrides/pos_store/pos_store.js",
            "nf_pos_toppings/static/src/overrides/pos_order_line/pos_order_line.js",
            "nf_pos_toppings/static/src/overrides/orderline/orderline.xml",
            # "nf_pos_toppings/static/src/overrides/orderline/orderline.js",
            "nf_pos_toppings/static/src/apps/css/nf_topping_orderline.css",
            "nf_pos_toppings/static/src/overrides/order_summary/order_summary.js",
        ],
    },
    "images": ["static/description/background.gif"],
    "application": False,
    "installable": True,
    "auto_install": False,
    "price": 35.99,
    "currency": "EUR",
}
