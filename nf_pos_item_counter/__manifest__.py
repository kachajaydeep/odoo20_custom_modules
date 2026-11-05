# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Item Counter",
    "summary": """
        pos order line count pos orderline count pos quantity count pos product count pos product total pos total line count pos product total pos prodcut counter orderline total pos product quantity count pos product quantity total quantity product pos line total  odoo pos item counter odoo point of sale counter odoo pos product line counter odoo pos quantity counter odoo pos total quantity odoo pos total items odoo retail pos odoo supermarket pos odoo grocery pos odoo pos order counter odoo pos line count odoo pos item count odoo pos module odoo apps store
    """,
    # "post_init_hook": 'post_init_hook',
    "description": """
        Display the total product lines and total product quantity in Odoo Point of Sale. Configure item counters from POS settings and monitor orders with live updates for faster, more accurate checkout.
    """,
    "data": [
        "views/res_config_settings_view.xml",
        "views/pos_order_receipt_view.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_item_counter/static/src/overrides/pos_order/pos_order.js",
            "nf_pos_item_counter/static/src/overrides/order_display/order_display.xml",
        ]
    },
    "author": "NextFlowIT",
    "license": "OPL-1",
    "category": "Point of sale",
    "website": "https://www.nextflow.in",
    "depends": ["point_of_sale"],
    "version": "20.0.1",
    "images": ["static/description/background.gif"],
    "application": True,
    "installable": True,
    "auto_install": False,
    "price": 10.2,
    "currency": "USD"
}
