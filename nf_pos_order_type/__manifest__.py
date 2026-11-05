# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.
{
    "name": "Pos Order Type",
    "summary": """Odoo POS Order Type, POS order categorization, Odoo restaurant POS, takeaway order management, delivery order tracking, POS workflow optimization, Odoo multi-store POS, POS analytics, instant delivery POS sale type different types of order delivery order in pos pos delivery order delivery address customer home delivery dine in dine-in restaurant food delivery ordering system food home delivery""",
    "description": """ Enhance your Odoo POS with the POS Order Type module - categorize orders as dine-in, takeaway, or delivery, streamline checkout, and gain insightful sales analytics. """,
    "data": [
        "security/ir.access.csv",
        "views/pos_order_type_view.xml",
        "views/res_config_settings_inherit_view.xml",
        "views/pos_order_inherit_view.xml",
        "receipt/pos_order_receipt.xml",
    ],
    "post_init_hook": "post_init_hook",
    "author": "NextFlowIT",
    "company": "NextFlow Technology",
    "maintainer": "NextFlow Technology",
    "website": "https://www.nextflow.in",
    "depends": ["point_of_sale"],
    "version": "20.0.1",
    "license": "OPL-1",
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_order_type/static/src/apps/order_type_buttons/order_type_buttons.xml",
            "nf_pos_order_type/static/src/apps/order_type_buttons/order_type_buttons.js",
            "nf_pos_order_type/static/src/apps/order_type_popup/order_types_popup.js",
            "nf_pos_order_type/static/src/apps/order_type_popup/order_types_popup.xml",
            "nf_pos_order_type/static/src/overrides/pos_order/pos_order.js",
            # "nf_pos_order_type/static/src/overrides/pos_order_receipt/pos_order_receipt.xml",
        ],
    },
    "images": ["static/description/background.gif"],
    "application": False,
    "installable": True,
    "auto_install": False,
    "price": 24.99,
    "currency": "EUR",
}
