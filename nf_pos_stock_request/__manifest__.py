# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.
{
    "name": "POS Stock Request",
    'summary': """odoo pos stock request point of sale stock real-time inventory internal transfers stock requests pos inventory management warehouse integration inventory approval stock tracking odoo pos module multi-store pos stock notifications point of sale stock request point of sale real time inventory transfer point of sale inventory management inventory management from point of sale inventory manage from pos stock request from point of sale""",
    'post_init_hook': 'post_init_hook',
    'description': """POS Stock Request module for Odoo 19 allows real-time stock visibility in POS, enables stock requests from stores, tracks request history, and automates internal transfers. Improve inventory management and streamline POS operations.""",
    "version":"20.0.1",
    "data":[
        'views/res_config_settings_inherited_view.xml',
    ],
    'author': 'NextFlowIT',
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'https://www.nextflow.in',
    'assets':{
      'point_of_sale._assets_pos': [
        "nf_pos_stock_request/static/src/apps/control_buttons/control_buttons.xml",
        "nf_pos_stock_request/static/src/apps/control_buttons/control_buttons.js",
        "nf_pos_stock_request/static/src/apps/popup/stock_request_popup/stock_request_popup.js",
        "nf_pos_stock_request/static/src/apps/popup/stock_request_popup/stock_request_popup.xml",
        "nf_pos_stock_request/static/src/apps/popup/stock_history_popup/stock_history_popup.js",
        "nf_pos_stock_request/static/src/apps/popup/stock_history_popup/stock_history_popup.xml",
        "nf_pos_stock_request/static/src/apps/screens/nf_stock_picking_history.js",
        "nf_pos_stock_request/static/src/apps/screens/nf_stock_picking_history.xml",
        "nf_pos_stock_request/static/src/apps/popup/stock_move_popup/stock_move_popup.js",
        "nf_pos_stock_request/static/src/apps/popup/stock_move_popup/stock_move_popup.xml",
        "nf_pos_stock_request/static/src/overrides/pos_order/pos_store.js",
      ],
    },
    "depends":['hr','point_of_sale','nf_pos_stock_info','stock'],
    "images": ["static/description/background.gif"],
    "license":'OPL-1',
    'application': False,
    'installable': True,
    'auto_install': False,
}