# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.
{
    "name": "Price Checker Kiosk",
    'summary': """odoo price checker kiosk product information kiosk barcode scanner odoo price checker module product details odoo kiosk inventory lookup customizable display light dark mode Odoo employee kiosk customer kiosk get product details using barcode get product details using the default code get all product details using the product barcode get all product details using the product default code""",
    'post_init_hook': 'post_init_hook',
    'description': """The Price Checker Kiosk module in Odoo offers a simple and efficient way to view product details. Scan or enter barcodes to instantly access product name, price, stock quantity, variants, and more. Supports customizable displays and light/dark modes for a seamless user experience.""",
    "version":"20.0.1",
    "data":[
        'security/ir.access.csv',
        'security/product_configuration_access.xml',
        'views/res_config_setting_inherited_view.xml',
        'views/nf_price_checker_template.xml',
    ],
    'author': 'NextFlowIT',
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'https://www.nextflow.in',
    "assets":{
        'nf_price_checker_kiosk.assets_kiosk':[
            'nf_price_checker_kiosk/static/src/js/nf_price_checker_kiosk.js',
            'nf_price_checker_kiosk/static/src/scss/nf_price_checker_kiosk.scss',
            'nf_price_checker_kiosk/static/src/xml/nf_price_checker_kiosk.xml',
        ],
    },
    "depends":['web','stock','account','sale_management'],
    "images": ["static/description/background.gif"],
    "license":'OPL-1',
    'application': False,
    'installable': True,
    'auto_install': False,
}