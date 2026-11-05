# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

{
    'name' : 'Point Of Sale default Customer Invoice || Auto invoice print',
    'summary': '''
        Point Of Sale default invoice customer invoice auto print direct print auto generate invoice auto invoice invoice auto pos invoice pos direct invoice print  
        auto print print auto invoice default customer pos invoice print pos invoice print point of sale invoice print auto print invoice default customer auto print partner print invoice auto pos order print invoice odoo pos invoice odoo auto invoice printodoo pos auto invoiceodoo point of sale invoice odoo customer invoice odoo pos billing odoo pos invoice automation odoo retail invoice odoo pos quick invoice odoo auto print customer invoiceodoo invoice printing odoo pos receipt invoice odoo default invoice customer odoo customer billing odoo pos invoicing odoo point of sale billing odoo retail management odoo pos customization odoo invoice generation odoo pos customer invoice odoo automatic invoicing odoo pos productivity odoo accounting integration odoo retail solution odoo pos module
    ''',
    'author' : 'NextFlowIT',
    "license": "OPL-1",
    'description' : """
        This App is help you to set default invoice for some customer and also you can auto print invoice from pos.
        Automatically generate and print customer invoices directly from Odoo POS. Set default invoice customers, enable auto invoice printing, quick invoice generation, and one-click invoice printing from POS. Improve billing speed, reduce manual work, and streamline retail operations with automated POS invoicing.    
    """,
    'category' : "Point of sale",
    'website' : '',
    'depends' :['point_of_sale'],
    'version' : '20.0.1',
    'data' :[  
        'views/nf_pos_customer.xml',
        'views/res_config_settings_view.xml',
     ],
    'assets': {
        'point_of_sale._assets_pos': [ 
            'nf_pos_default_customer_invoice/static/src/js/print.min.js',
            'nf_pos_default_customer_invoice/static/src/overrides/order_payment_validation/order_payment_validation.js',
        ],
     },
    "images": ["static/description/background.png"],
    "price": 21.42,
    'installable' : True,
    'application' : True,
    'auto_install' : False,
    "currency": "EUR"
}
