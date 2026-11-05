# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.
{
    "name":"POS Keyboard Shortcuts",    
    "summary": """
        pos shortcut keyboard pos shortcuts keyboard pos keyboard shortcut pos keyboard shortcuts odoo pos keyboard shortcuts hotkeys odoo keyboard shortcuts point of sale shortcuts pos productivity fast pos checkout odoo retail cashier pos navigation pos keyboard pos shortcut keys pos efficiency retail module apps point of sale keyboard controls
    """,
    "post_init_hook": 'post_init_hook',
    "description": """ 
        Improve your Odoo Point of Sale workflow with customizable keyboard shortcuts. Navigate POS faster, create orders quickly, process payments, and reduce mouse usage for a faster checkout experience.
    """,
    "data":[
        'security/ir.access.csv',
        'views/res_config_view.xml',
    ],
    "assets": {
        'web.assets_backend': [
            'nf_pos_keyboard_shortcuts/static/src/scss/shortcut_key_field.scss',
            'nf_pos_keyboard_shortcuts/static/src/js/shortcut_key_field.js',
            'nf_pos_keyboard_shortcuts/static/src/xml/shortcut_key_field.xml',
        ],
        'point_of_sale._assets_pos':[
            'nf_pos_keyboard_shortcuts/static/src/xml/*',
            'nf_pos_keyboard_shortcuts/static/src/js/*',
            'nf_pos_keyboard_shortcuts/static/src/scss/shortcut_popup.scss',
        ]
    },
    "author": 'NextFlowIT',
    "company": 'NextFlow Technology',
    "maintainer": 'NextFlow Technology',
    "website": 'https://www.nextflow.in',
    "depends":['point_of_sale'],
    "images": ["static/description/background.gif"],
    "version":"20.0.1",
    "license":"OPL-1",
    "application": True,
    "installable": True,
    "auto_install": False,
    "price": 25.00,
    "currency": "USD"
}