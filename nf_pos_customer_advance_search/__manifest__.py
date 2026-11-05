# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.
{
    "name": "Point of sale Customer Advance Search",
    "summary": """pos advance search quick search customer in pos quick search customer quick create customer from pos customer advance search serch customer by name search customer by mobile  """,
    "post_init_hook": "post_init_hook",
    "description": """The Pos Customer Selection module for Odoo POS automatically selects a customer when a customer is chosen. It improves POS workflow, reduces manual customer switching, and ensures efficient transaction handling.""",
    "version": "20.0.1",
    "author": "NextFlowIT",
    "company": "NextFlow Technology",
    "maintainer": "NextFlow Technology",
    "website": "https://www.nextflow.in",
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_customer_advance_search/static/src/overrides/navbar/navbar.xml",
            "nf_pos_customer_advance_search/static/src/overrides/navbar/navbar.scss",
            "nf_pos_customer_advance_search/static/src/overrides/navbar/navbar.js",
        ],
    },
    "depends": ["pos_hr", "hr", "point_of_sale"],
    "images": ["static/description/background.gif"],
    "license": "OPL-1",
    "application": False,
    "installable": True,
    "auto_install": False,
    "price": 12.00,
    "currency": "USD",
}
