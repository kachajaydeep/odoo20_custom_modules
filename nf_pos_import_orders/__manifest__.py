# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Import Orders",
    "summary": """
        odoo pos import orders odoo pos excel import import pos orders xlsx pos order import bulk pos order import pos data migration import sales orders pos odoo point of sale import pos session import pos payment import excel pos import odoo retail import pos historical orders odoo pos migration pos xlsx upload import excel import pos order excel import order excel order import excel import pos xlsx import order xlsx import pos xlsx import xlsx
    """,
    "post_init_hook": "post_init_hook",
    "description": """
        Import Point of Sale orders into Odoo from Excel (XLSX) files with a simple import wizard. Automatically assign fallback POS sessions and payment methods, validate data, and bulk import orders with detailed import results for easy POS migration and synchronization.
    """,
    "data": [
        "security/ir.access.csv",
        "wizard/pos_import_wizard_view.xml",
        "views/pos_import_menu.xml",
    ],
    "author": "NextFlowIT",
    "company": 'NextFlow Technology',
    "maintainer": 'NextFlow Technology',
    "category": "Point of sale",
    "website": "https://www.nextflow.in",
    "depends": ["point_of_sale", "hr"],
    "version": "20.0.1",
    "license": "OPL-1",
    "images": ["static/description/background.gif"],
    "application": True,
    "installable": True,
    "auto_install": False,
    "price": 40.50,
    "currency": "USD"
}
