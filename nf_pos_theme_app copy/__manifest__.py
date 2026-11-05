# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

{
    'name' : 'Point Of Sale theme | Pos theme',
    'summary': """
        Odoo POS Theme Odoo Point of Sale Theme Odoo POS UI Odoo POS Design Odoo POS Interface Modern POS Theme Odoo POS Customization Odoo POS Frontend Odoo POS Layout Odoo POS User Interface Odoo POS UX Odoo Retail POS Theme Odoo POS Styling Odoo POS Dashboard Odoo Apps Point of Sale Theme Odoo POS Enhancement Responsive POS Theme Point Of Sale theme pos theme point of sale theme odoo pos theme chang pos layout change layout 
        point of sale theme pos theme odoo pos theme odoo point of sale theme odoo pos customization odoo pos ui odoo pos interface modern pos theme retail pos theme restaurant pos theme cafe pos theme supermarket pos theme pharmacy pos theme bakery pos theme shop pos theme grocery store pos retail store pos fashion store pos electronics store pos convenience store pos restaurant management pos restaurant theme food service pos bar pos system hotel restaurant pos quick service restaurant pos fine dining pos multi store pos cashier interface pos dashboard odoo retail management odoo restaurant pos odoo shop management odoo restaurant management odoo retail solution point of sale design pos user interface pos layout retail automation odoo apps nextflow technology odoo module
        """,
    'author' : 'NextFlowIT',
    "license": "OPL-1",
    'description' : """
        Upgrade your Odoo Point of Sale with a modern sleek and user-friendly POS theme. Improve the POS interface with a clean layout stylish buttons refined colors responsive design and an enhanced user experience without changing the core Odoo POS functionality.
        Transform your Odoo Point of Sale with a modern POS Theme designed for retail stores, supermarkets, restaurants, cafés, bakeries, pharmacies, and all retail businesses. Improve the user experience with a clean interface, enhanced navigation, faster order processing, and an attractive POS layout.
        """,
    'category': 'Point of sale',
    'website' : '',
    'depends' :['point_of_sale'],
    'version' : '20.0.1',
    'data' :[   
        'security/ir.access.csv',
        'views/nf_pos_theme_setting.xml',
        'views/pos_config.xml'
    ],
    'assets': {
        'web._assets_primary_variables': [
            'nf_pos_theme_app/static/src/scss/nf_theme_variables.scss'
        ],
        'point_of_sale._assets_pos': [
           'nf_pos_theme_app/static/src/scss/pos.scss',
           'nf_pos_theme_app/static/src/js/overrides/orderline/orderline.xml',
           'nf_pos_theme_app/static/src/js/overrides/orderline/orderline.js',
           'nf_pos_theme_app/static/src/js/overrides/productscreen/listComponent/*',
           'nf_pos_theme_app/static/src/js/overrides/navbar/navbar.xml',
           'nf_pos_theme_app/static/src/js/overrides/productscreen/ProductScreen.js',
           'nf_pos_theme_app/static/src/js/overrides/productscreen/ProductScreen.xml',
           'nf_pos_theme_app/static/src/js/overrides/PaymentScreen/PaymentScreen.js',
           'nf_pos_theme_app/static/src/js/overrides/PaymentScreen/PaymentScreen.xml',
           'nf_pos_theme_app/static/src/js/overrides/ActionpadWidget/ActionpadWidget.xml',
           'nf_pos_theme_app/static/src/js/overrides/ActionpadWidget/Actionwidget.scss',
           'nf_pos_theme_app/static/src/js/overrides/productCard/productCard.xml',
           'nf_pos_theme_app/static/src/js/overrides/productCard/productCard.js',
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
