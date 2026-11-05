# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

{
    'name':"POS Auto Lock",
    'summary': """ 
        odoo pos auto lock odoo pos auto screen pos auto lock screen pos lock screen pos odoo pos saver screen odoo pos inactivity timeout odoo point of sale auto lock odoo pos security odoo pos session lock odoo pos idle timeout odoo pos login screen odoo pos screen lock odoo pos configuration pos point of sale auto lock pos inactivity lock pos security module nextflowit odoo module retail pos security unattended pos protection odoo apps store POS module
    """,
    'post_init_hook': 'post_init_hook',
    'description': """ 
        Enhance Odoo Point of Sale security with the POS Auto Lock module. Configure custom inactivity timeouts for the Saver Screen and Login Screen, automatically lock unattended POS sessions, replace default Odoo idle timeout behavior, and protect your retail operations with easy POS configuration.
    """,
    'data':[
       "views/pos_config.xml",
    ],
    'assets':{
        'point_of_sale._assets_pos': [
            "nf_pos_auto_lock/static/src/js/auto_lock_config.js",
            "nf_pos_auto_lock/static/src/xml/saver_screen.xml",
        ],
    },
    'author': 'NextFlowIT',
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'https://www.nextflow.in',
    'depends':['point_of_sale'],
    'version':"20.0.1",
    'license':"OPL-1",
    'images': ["static/description/background.gif"],
    'application': True,
    'installable': True,
    'auto_install': False,
    'price': 00.00,
    'currency': "USD"
}