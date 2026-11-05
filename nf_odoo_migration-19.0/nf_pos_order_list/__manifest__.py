# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

{
    'name' : 'Point Of Sale Order list',
    'summary': """ point of sale order management pos order tracking order list software retail order management pos order processing point of sale order tracking system efficient order lists for pos retail order fulfillment order management solutions pos transaction tracking streamlined pos orders point of sale inventory management order processing software pos sales order system point of sale order workflow retail pos order history order list optimization pos order automation e-commerce pos order system in-store order list solutions pos order list point of sale order list list orders list order """,
    'author' : 'NextFlowIT',
    "license": "OPL-1",
    'description' : """ point of sale order list custom screen  """,
    'category' : "Point of sale",
    'website' : '',
    'depends' :['point_of_sale'],
    'version' : '0.0.1',
    'data' :[   
        'views/res_pos_config.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_pos_order_list/static/src/apps/store/pos_store.js',
            'nf_pos_order_list/static/src/screens/*/*',
            'nf_pos_order_list/static/src/apps/buttons/**/*',
            # 'nf_pos_order_list/static/src/screens/order_list/*',
            # 'nf_pos_order_list/static/src/apps/popups/nf_order_lines/*',
            # 'nf_pos_order_list/static/src/apps/store/pos_store.js'
        ]
     },
    "images": ["static/description/background.gif", ],
    "price": 25.42,
    'installable' : True,
    'application' : True,
    "currency": "EUR"
}
