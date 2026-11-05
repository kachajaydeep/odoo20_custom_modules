# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

{
    'name' : 'Point Of Sale theme | Pos theme',
    'summary': """Odoo POS Theme Odoo Point of Sale Theme Odoo POS UI Odoo POS Design Odoo POS Interface Modern POS Theme Odoo POS Customization Odoo POS Frontend Odoo POS Layout Odoo POS User Interface Odoo POS UX Odoo Retail POS Theme Odoo POS Styling Odoo POS Dashboard Odoo Apps Point of Sale Theme Odoo POS Enhancement Responsive POS Theme Point Of Sale theme pos theme point of sale theme odoo pos theme chang pos layout change layout """,
    'author' : 'NextFlowIT',
    "license": "OPL-1",
    'description' : """Upgrade your Odoo Point of Sale with a modern sleek and user-friendly POS theme. Improve the POS interface with a clean layout stylish buttons refined colors responsive design and an enhanced user experience without changing the core Odoo POS functionality.""",
    'category': 'Point of sale',
    'website' : '',
    'depends' :['point_of_sale'],
    'version' : '20.0.0.3',
    'data' :[   
        'security/ir.model.access.csv',
        'views/nf_pos_theme_setting.xml',
        'views/pos_config.xml'
    ],
    'assets': {
        'web._assets_primary_variables': [
            'nf_pos_theme_app/static/src/scss/nf_theme_variables.scss'
        ],
        'point_of_sale._assets_pos': [
           'nf_pos_theme_app/static/src/scss/pos.scss',
           'nf_pos_theme_app/static/src/js/overrides/models/orderline.js',
           'nf_pos_theme_app/static/src/js/overrides/orderline/pos_card.xml',
           'nf_pos_theme_app/static/src/js/overrides/orderline/orderline.js',
           'nf_pos_theme_app/static/src/js/overrides/productscreen/listComponent/*',
           'nf_pos_theme_app/static/src/js/overrides/productscreen/ProductScreen.js',
           'nf_pos_theme_app/static/src/js/overrides/navbar/navbar.xml',
           'nf_pos_theme_app/static/src/js/overrides/productscreen/productscreen.xml',
           'nf_pos_theme_app/static/src/js/overrides/ActionpadWidget/ActionpadWidget.xml',
           'nf_pos_theme_app/static/src/js/overrides/ActionpadWidget/ActionWidget.js',
           'nf_pos_theme_app/static/src/js/overrides/PaymentScreen/paymenbtscreen.js',
           'nf_pos_theme_app/static/src/js/overrides/PaymentScreen/PaymentScreen.xml',
           'nf_pos_theme_app/static/src/js/overrides/ActionpadWidget/Actionwidget.scss',
           'nf_pos_theme_app/static/src/js/overrides/productCard/productCard.xml',
           'nf_pos_theme_app/static/src/js/overrides/productCard/product_card.js',
           'nf_pos_theme_app/static/src/js/overrides/orderline_note_button/orderline_note_button.xml',
           'nf_pos_theme_app/static/src/js/overrides/order_display/order_display.xml',
        ]
     },
    "images": ["static/description/background.gif", ],
    'post_init_hook': 'post_init_hook',
    "price": 75.42,
    'installable' : True,
    'application' : True,
    "currency": "EUR"
}
