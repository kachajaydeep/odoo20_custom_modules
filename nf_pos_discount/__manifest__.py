# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Discount || Point of sale Amount/Percentage discount ",
    "summary": """ 
        POS discount Amount discount Percentage discount POS calculator Odoo POS enhancement POS retail discount Fast billing POS Dynamic discount Odoo Odoo POS addon Discount automation POS cashiers tools Odoo 18 POS module Billing accuracy Point of sale discounting Price-based discount module odoo pos discount, pos discount module odoo, odoo 19 pos discount, apply discount in odoo pos, pos percentage discount odoo, pos fixed discount odoo, odoo point of sale discount
        point of sale global discount line discount apply discount base on amount pos discount amount discount global discount price discount line price discount remove discount global auto calculate discount pos global discount pos line discount pos discount odoo pos discount odoo point of sale discount module pos amount discount odoo pos percentage discount odoo odoo pos fixed amount discount odoo pos auto percentage calculation odoo pos dynamic discount odoo pos discount calculator odoo 18 pos discount module odoo pos improve discount odoo pos custom discount feature odoo pos cashier discount tool odoo retail discount module odoo pos billing discount odoo pos promotion discount odoo pos fast discount entry odoo pos discount enhancement odoo pos discount by amount odoo pos discount by percentage odoo pos flexible discount system odoo pos smart discount odoo pos amount to percent odoo pos checkout discount odoo pos addon discount module pos discount extension odoo odoo pos price-based discount pos multi discount
        odoo pos global discount odoo point of sale discount pos discount amount pos percentage discount global discount pos line discount pos pos promotion retail discount odoo odoo pos pricing pos discount management odoo 18 pos odoo retail module pos customer discount odoo pos extensions odoo apps store pos product discount global discount pos order discount pos discount
    """,
    "author": "NextFlowIT",
    "license": "OPL-1",
    "description": """ 
        apply disocunt base on amount also apply global disocunt in point of sale.
        Apply global and line discounts in Odoo Point of Sale using fixed amounts or percentages. Display total discount, optional base price, automatic calculations, and remove all discounts with one click for a faster.
    """,
    "category": "Point of sale",
    "website": "",
    "depends": ["point_of_sale"],
    "version": "20.0.1",
    "data": [
        "views/res_pos_config.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_discount/static/src/apps/models.js",
            "nf_pos_discount/static/src/apps/contro_buttons/*",
            "nf_pos_discount/static/src/apps/popups/numberPopup/*",
            "nf_pos_discount/static/src/overrides/OrderDisplay/*",
        ],
    },
    "images": [
        "static/description/background.gif",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": True,
    "price": 25.42,
    "auto_install": False,
    "currency": "EUR",
}