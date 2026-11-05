# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Pos Close Session From Backend",
    "summary": """odoo pos pos session management close pos session backend pos ending balance cash reconciliation pos workflow odoo module pos audit odoo point of sale multi-session pos pos management odoo backend pos automation pos close session from backend pos session close from backedn forgot to close session forgot to close pos session""",
    "description": """allows seamless management of POS sessions from the Odoo backend. Track, validate, and close POS sessions with accurate ending balances, error prevention, and audit-friendly operations. Streamline your POS workflow and improve operational control.""",
    "version": "20.0.1",
    "post_init_hook": "post_init_hook",
    "author": "NextFlowIT",
    "company": "NextFlow Technology",
    "maintainer": "NextFlow Technology",
    "website": "https://www.nextflow.in",
    "data": [
        "security/ir.access.csv",
        "wizard/nf_pos_session_closing_balence.xml",
        "views/pos_session_inherited_view.xml",
    ],
    "depends": ["point_of_sale"],
    "license": "OPL-1",
    "images": [
        "static/description/background.gif",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
    "price": 20,
    "currency": "EUR",
}
