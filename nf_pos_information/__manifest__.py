# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.
{
    "name":"Pos Product Information",
    'summary': """ 
        odoo pos product information odoo pos product details module odoo point of sale product information odoo pos product info popup odoo pos product details view odoo pos product description module odoo retail pos product information odoo pos product information addon odoo pos customization module odoo pos retail product details odoo point of sale enhancement odoo pos product data display odoo pos product information app odoo pos product details feature odoo pos product information odoo app odoo pos product information plugin odoo retail management pos module odoo apps pos customization odoo pos product info integration odoo erp pos product information module best odoo pos product information module odoo pos product details app product information popup in odoo pos show product details in odoo pos screen odoo retail pos product information feature odoo pos customization product details odoo pos product information for retail stores odoo point of sale product information addon odoo pos product details extension odoo pos product information software Odoo POS Prodcut InformationProduct Information in Odoo POS Odoo POS Product Details Odoo POS Product Info Odoo POS Product Description Odoo POS Product Data Odoo POS Product Information App Odoo POS Product Information Module Odoo POS Product Information Addon Product Information pos product information pos product details pos product info popup pos product details view pos product description""",
    'post_init_hook': 'post_init_hook',
    'description': """ 
        Enhance your Odoo Point of Sale with the POS Product Information module. Instantly view detailed product information directly in the POS interface including price, stock, product details, and other useful data to help cashiers make faster and more accurate sales decisions.
    """,
    "data":[
       
    ],
    'author': 'NextFlowIT',
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'https://www.nextflow.in',
    "depends":['point_of_sale'],
    "version":"20.0.1",
    "license":"OPL-1",
    "images": ["static/description/background.gif"],
    'assets':{
        'point_of_sale._assets_pos': [
           'nf_pos_information/static/src/overrides/controlbuttons/*',
           'nf_pos_information/static/src/apps/popups/productpopup/*',
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
    "price": 5.0,
    "currency": "USD"
}