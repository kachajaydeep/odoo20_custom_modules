# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

{
    'name' : 'Point Of Sale Realtime Stock Update',
    'summary': """
        point of sale realtime stock upadte pos realtime stock pos stock update pos stock pos update pos update stock display stock pos stock display pos inventory pos stock inventory pos realtime stock update
        odoo pos realtime stock update pos live stock update point of sale stock synchronization realtime inventory update pos stock refresh odoo pos inventory live product quantity pos automatic stock update odoo inventory sync sale order stock update purchase order stock update stock transfer update warehouse stock sync retail inventory management odoo pos module odoo apps nextflow technology
    """,
    'author' : 'NextFlowIT',
    "license": "OPL-1",
    'description' : """ 
        This module is use to display current warehouse stock in product screen, also update qty in all session whren any user create sale order from Pos 
        Keep POS inventory synchronized in real time with Odoo. Automatically update product stock in Point of Sale after POS Orders, Sales Orders, Purchase Orders, Stock Transfers, and manual inventory adjustments. Display live stock quantities on the POS product screen.
        """,
    'post_init_hook': 'post_init_hook',
    'category' : "Point of sale",
    'website' : '',
    'depends' :['point_of_sale', 'nf_pos_stock_info'],
    'version' : '20.0.1',
    'data' :[   
            'views/pos_res_settings.xml',
            ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_pos_reltime_stock_update/static/src/overrides/**/*',
            'nf_pos_reltime_stock_update/static/src/js/PosBus.js',
        ]
     },
    'images': ['static/description/background.gif'],
    "price": 70.42,
    'installable' : True,
    'application' : True,
    "currency": "EUR"
}
