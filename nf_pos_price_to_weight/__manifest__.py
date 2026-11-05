# -*- coding: utf-8 -*-
# Part of NextFlowIT.
{
    'name' : 'POS Price To Weight',
    'summary': 'This module increase your Point of sale functionality. Allow to scan Barcode with price and to compute according Quantity. Point of sale price to weight, pos price to weight, price to weight, weight to price, ',
    'author' : 'NextFlowIT',
    "license": "OPL-1",
    'description' : """ This module Allow to scan Barcode with price and to compute according Quantity. This module is usefull in shops with products scaled, to manage correctly stock quantities. """,
    'category' : "Point of Sale",
    'website' : '',
    'depends' :['point_of_sale'],
    'version' : '20.0.1',
    'demo': [
        'demo/demo_product.xml',
    ],
    'data' :[   
        'data/barcode_rule.xml',
        'views/view_pos_config.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_pos_price_to_weight/static/src/js/product_screen.js',
        ]
    },
    "images": ["static/description/background.gif", "static/description/background.png"],
    "price": 22. ,
    'installable' : True,
    'application' : True,
    'auto_install' : False,
    "currency": "EUR"
}
