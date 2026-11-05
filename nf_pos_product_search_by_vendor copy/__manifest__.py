# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Search Product By Vendor",
    "summary": """
        search product by vendor product vandor search in pos search vendor pos purchase product search pos vendors pos point of sale product search by vendor
        odoo pos point of sale pos vendor filter pos supplier filter search product by vendor pos product search odoo vendor filter odoo supplier filter pos product filter multi vendor pos odoo pos product filter supplier product search vendor product search
    """,
    "post_init_hook": 'post_init_hook',
    "description": """ 
        search product by vendor product vandor search in pos search vendor pos purchase product search pos vendors pos point of sale product search by vendor 
        Filter and search Odoo POS products by vendor or supplier. Quickly find products from specific vendors directly in the POS product screen.
    """,
    "data": [
        'views/res_config_settings_inherit_view.xml',
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_product_search_by_vendor/static/src/overrides/navbar/navbar.xml",
            "nf_pos_product_search_by_vendor/static/src/overrides/navbar/navbar.js",
            "nf_pos_product_search_by_vendor/static/src/overrides/navbar/navbar.scss",
            "nf_pos_product_search_by_vendor/static/src/overrides/pos_store/pos_store.js",
            ],
    },
    "author" : 'NextFlowIT',
    "company": 'NextFlow Technology',
    "maintainer": 'NextFlow Technology',
    "website": 'https://www.nextflow.in',
    "support": "support@nextflow.in",
    "category": "Point Of Sale",
    "license": "OPL-1",
    "version": "20.0.1",
    "depends": ["point_of_sale","purchase"],
    "images": ["static/description/background.gif" ],
    "price": 15.42,
    "application": True,
    "installable": True,
    "auto_install": False,
    "currency": "EUR"
}
