# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.

{
    "name": "Point Of Sale Search Product By Vendor",
    'author' : 'NextFlowIT',
    "support": "",
    "category": "Point Of Sale",
    "license": "OPL-1",
    "summary": "search product by vendor product vandor search in pos search vendor pos purchase product search pos vendors pos point of sale product search by vendor",
    "description": """ search product by vendor product vandor search in pos search vendor pos purchase product search pos vendors pos point of sale product search by vendor """,
    'post_init_hook': 'post_init_hook',
    "version": "20.0.1",
    "depends": ["point_of_sale","purchase"],
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
    "images": ["static/description/background.gif" ],
    "price": 15.42,
    'installable' : True,
    'application' : True,
    "currency": "EUR"
}
