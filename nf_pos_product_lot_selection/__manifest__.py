# -*- coding: utf-8 -*-
# Copyright (C) NextFlowIT
{
    'name' : 'POS Product lot selection',
    'summary': """
      point of sale lot selection pos lot pos refund pos lot refund lot pos multi lot select pos select lot lot select pos multi lot select pos multi lot selection pos lot number selection pos lot selection pos serial selection pos serial number selection os serial selection
      odoo pos odoo point of sale pos lot selection product lot selection lot management pos lot management odoo lot number pos lot number serial number pos odoo inventory lot pos inventory lot tracking product tracking pos refund lot odoo pos module odoo pos lot multiple lot selection custom lot quantity odoo pos lot selection odoo pos module odoo point of sale odoo inventory lot management odoo pos customization odoo pos customization odoo developer odoo developer odoo development company odoo development company odoo pos solution odoo pos solution odoo inventory solution odoo implementation odoo implementation odoo partner odoo partner odoo pos development odoo pos development odoo lot tracking odoo serial number tracking pos lot management pos inventory management custom odoo pos module custom odoo module
      """,
    'description' : """ Manage product lots directly in Odoo Point of Sale. Select multiple lots, enter custom quantities, view available quantities in real time, print lot details, and simplify refunds.
      this app helps you in lot selection  
      """,
    'depends' :['point_of_sale', 'stock'],
    'data' :[
      'views/pos_config.xml',
    ],
    "assets":  {
      'point_of_sale._assets_pos': [
        'nf_pos_product_lot_selection/static/src/js/pos_store.js',
        'nf_pos_product_lot_selection/static/src/js/order_summary.js',
        'nf_pos_product_lot_selection/static/src/js/Screens/PaymentScreen.js',
        'nf_pos_product_lot_selection/static/src/popups/nf_select_lot_popup.js',
        'nf_pos_product_lot_selection/static/src/popups/nf_select_lot_popup.xml',
      ],
    },
    'author' : 'NextFlowIT',
    "license": "OPL-1",
    'category' : "Point of Sale",
    'website' : 'nextflow.in',
    'version' : '20.0.1',
    "images": ["static/description/background.gif", ],
    'installable' : True,
    'application' : True,
    'auto_install' : False,
    "price": 30.42,
    "currency": "EUR"
}
