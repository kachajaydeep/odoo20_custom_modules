# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Cash in Out Receipt",
    "summary": """ 
        pos cash in out receipt pos cash in receipt pos cash out receipt cash receipt in/out receipt in-out receipt pos in out receipt cash report cash in report pos cash in report z report total cash in/in-out total cash report pos cash receipt cash control session cash report out report in report in out report in/out report session report cash in out report as receipt cash in report receipt cash out report receipt  
        odoo pos cash in receipt odoo pos cash out receipt pos cash receipt point of sale cash in out odoo cash drawer receipt pos session cash report pos cash summary receipt cash in out printing odoo pos receipt pos cash management odoo pos cash control pos session report pos cash print receipt pos cash receipt print odoo cash in out
    """,
    "author": "NextFlowIT",
    "license": "OPL-1",
    "description": """ 
        pos cash in out receipt and total cash in out report 
        Automatically print Cash In and Cash Out receipts in Odoo POS. Generate session-wise Cash In/Out summary receipts, track cash movements, improve reconciliation, and enable configurable automatic receipt printing.    
    """,
    "category": "Point of sale",
    "website": "",
    "depends": ["point_of_sale"],
    "version": "20.0.1",
    "data": ["views/res_pos_settings.xml"],
    "assets": {
        "point_of_sale._assets_pos": ["nf_pos_cash_control_receipts/static/src/**/*"]
    },
    "images": [
        "static/description/background.gif",
    ],
    "post_init_hook": "post_init_hook",
    "price": 30.42,
    "installable": True,
    "application": True,
    "auto_install": False,
    "currency": "EUR",
}