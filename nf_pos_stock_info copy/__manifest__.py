# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

{
    'name' : 'Point Of Sale Display Stock',
    'summary': """ point of sale stock upadte pos stock pos update pos update stock display stock pos stock display pos inventory pos stock inventory pos stock update """,
    'author' : 'NextFlowIT',
    "license": "OPL-1",
    'description' : """ point of sale display stock  """,
    'category' : "Point of sale",
    'website' : '',
    'depends' :['point_of_sale','stock','pos_stock'],
    'version' : '20.0.1',
    'data' :[   
            'views/pos_res_settings.xml',
            ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_pos_stock_info/static/src/overrides/pos_store/pos_store.js',
            'nf_pos_stock_info/static/src/overrides/product_info_popup/product_info_popup.xml',
            'nf_pos_stock_info/static/src/overrides/product_info_popup/product_info_popup.scss',
            'nf_pos_stock_info/static/src/overrides/product_card/product_card.xml',
            'nf_pos_stock_info/static/src/overrides/product_card/product_card.js',
            'nf_pos_stock_info/static/src/overrides/product_card/product_card.scss',

        ]
     },
    "images": ["static/description/background.gif", ],
    'post_init_hook': 'post_init_hook',
    "price": 15.42,
    'installable' : True,
    'application' : True,
    "currency": "EUR"
}