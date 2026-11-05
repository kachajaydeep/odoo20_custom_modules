# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Direct Login",
    "summary": """
        odoo pos direct pos store login pos store direct login  login odoo pos auto login point of sale direct login odoo default pos store pos only user  odoo cashier login  odoo pos redirect  odoo retail pos  odoo pos user management  pos login automation  odoo apps  odoo community pos login employee pos login customer pos pos customer login cashier pos login cashier
    """,
    # "post_init_hook": "post_init_hook",
    "description": """
        Allow dedicated POS users to log in directly to their assigned Point of Sale in Odoo. Configure POS Only User and Default POS Store for faster cashier access, improved security, and a streamlined retail workflow.
    """,
    "data": [
        "views/res_user_views_inherit.xml",
        "views/res_config_view_inherited.xml",
        "views/web_login_view.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_direct_login/static/src/overrides/models/pos_store.js",
            "nf_pos_direct_login/static/src/overrides/screens/login_screen.xml",
            "nf_pos_direct_login/static/src/overrides/components/navbar.xml",
        ]
    },
    "author": 'NextFlowIT',
    "company": 'NextFlow Technology',
    "maintainer": 'NextFlow Technology',
    "website": 'https://www.nextflow.in',
    "category": "Point of sale",
    "depends": ['point_of_sale'],
    "version": "20.0.1",
    "license":"OPL-1",
    "images": ["static/description/background.gif"],
    "application": True,
    "installable": True,
    "application": True,
    "price": 15.00,
    "currency": "EUR",
}