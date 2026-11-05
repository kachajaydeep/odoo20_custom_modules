# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Secondary Uom",
    "summary": """
        odoo pos secondary uom pos units of measure for pos unit of measure unit pos uom product unit odoo secondary unit of measure odoo pos dual uom point of sale secondary uom odoo pos alternate uom odoo retail secondary unit odoo pos quantity conversion odoo pos multiple units odoo pos weight unit odoo pos packaging unit odoo pos selling by box odoo pos selling by carton odoo pos unit conversion units of measure pos
    """,
    # "post_init_hook": "post_init_hook",
    "description": """
        Manage products with a secondary unit of measure directly in Odoo Point of Sale. Sell products using primary and secondary UoM, improve billing accuracy, and simplify retail operations with automatic quantity conversion.
    """,
    "data": [
        "views/pos_config_view_nherited.xml",
        "views/product_view_inherit.xml",
        "views/pos_order_view_inherited.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_secondary_uom/static/src/overrides/component/orderline.js",
            "nf_pos_secondary_uom/static/src/overrides/controlButton/controlButtons.js",
            "nf_pos_secondary_uom/static/src/overrides/controlButton/controlButtons.xml",
        ]
    },
    "author": "NextFlowIT",
    "company": "NextFlow Technology",
    "maintainer":"NextFlow Technology",
    "category": "Point of sale",
    "website": "https://www.nextflow.in",
    "depends": ['point_of_sale', 'pos_stock'],
    "images": ["static/description/background.gif"],
    "version": "20.0.1",
    "license": "OPL-1",
    "application": True,
    "installable": True,
    "auto_install": False,
    "price": 25.00,
    "currency": "USD"
}