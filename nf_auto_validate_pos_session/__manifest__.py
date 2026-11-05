# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

{
    "name":"Auto Validate Pos Session",
    "summary": """ auto validate pos session automatic pos session validation pos automation pos session cron pos auto close pos session point of sale session automation retail automation pos session close pos session auto close automatically close pos session close pos automatic session close odoo auto validate pos session odoo pos session automation auto validate pos session odoo cron job odoo scheduled action odoo point of sale retail automation pos session close automatically everyday close pos session everyday close session
    """,
    "post_init_hook": 'post_init_hook',
    "description": """
        Automatically validate POS sessions in Odoo using scheduled Cron jobs. Enable Auto Session Validation for each POS configuration to reduce manual work, improve accounting workflow, and streamline daily POS operations.
    """,
    "data":[
        "data/auto_validate_session.xml",
        "views/pos_config.xml",
    ],
    "author": 'NextFlowIT',
    "company": 'NextFlow Technology',
    "maintainer": 'NextFlow Technology',
    "website": 'https://www.nextflow.in',
    "depends":['point_of_sale'],
    "version":"20.0.1",
    "license":"OPL-1",
    "images": ["static/description/background.gif"],
    "application": True,
    "installable": True,
    "auto_install": False,
    "price": 46.50,
    "currency": "USD"
}