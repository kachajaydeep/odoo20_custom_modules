# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'City wise Delivery Charges | Website Shipping Method Charges Based on City',
    'summary': '''
        website delivery charge delivery charge by city city wise delivery charge odoo website delivery charge odoo delivery cost management website sale delivery charge odoo ecommerce delivery fee delivery charges based on city city based shipping cost odoo website sale delivery odoo shipping charge module website delivery pricing odoo ecommerce shipping delivery fee calculation odoo customer city delivery charge dynamic delivery charge website checkout delivery charge odoo website shipping cost delivery charge automation odoo ecommerce customization shipping rules by city website order delivery fee odoo website order delivery delivery management odoo shipping charge configuration city wise shipping charges odoo delivery integration ecommerce delivery solution odoo website module nextflow technology odoo module
        odoo shipping charges city-based shipping odoo delivery cost by city shipping method pricing per city odoo city-wise shipping odoo shipping by location odoo city shipping configuration odoo region-specific delivery dynamic shipping cost odoo odoo shipping city filter location-based charges odoo smart shipping rules odoo shipping zones odoo module city-level pricing odoo multi-city shipping odoo odoo shipping rules regional shipping costs odoo zone-based delivery charges odoo location-based shipping odoo odoo delivery method by city odoo website shipping module odoo ecommerce shipping charges online store delivery charges odoo odoo webshop shipping by city odoo checkout shipping calculator odoo ecommerce city delivery cost delivery fees by city odoo webshop odoo cart shipping cost rules odoo website delivery configuration city-based checkout pricing odoo how to add shipping charges by city odoo best odoo module for city-based shipping odoo app for city-wise delivery charges advanced shipping rules in odoo odoo module for custom delivery fees shipping by customer city odoo per-city shipping odoo city-specific courier rates odoo odoo advanced shipping logic region-wise delivery fee configuration odoo Shipping method charges based on city wise delivery charge website city delivery charge state wise delivery chage state country city state delivery charge country delivery charge website shipping method website city wise shipping charges website city shipping charge city delivery fee country delivery fee state delivery fee city shipping fee
        odoo city delivery charges website shipping charges delivery charges by city city wise shipping website delivery fee odoo delivery cost delivery pricing by city website checkout delivery charge shipping method charges sales order delivery charge pos delivery charges multi city delivery local delivery charges delivery fee automation shipping cost based on city odoo ecommerce delivery delivery carrier charges multi company delivery charges odoo shipping module website shipping method based on city
    ''',
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'description': """ 
        Easily configure city-wise shipping charges for your Odoo sales and eCommerce platform. This module allows you to define shipping method pricing per city, giving you full control over delivery costs based on customer location.  
        Automatically apply delivery charges based on customer city in Odoo. Configure city-wise shipping fees for Website, Sales Orders, with multi-company support and automated delivery charge calculation.
        """,
    'category': "Website/Website",
    'website': 'nextflow.in',
    'depends': ['website', 'delivery', 'website_sale',],
    'version': '0.0.1',
    'data': [
        'security/ir.access.csv',
        'views/nf_city.xml',
        'views/delivery.xml',
        'views/partner.xml',
        'views/templates.xml',
    ],
    'assets': {
       'web.assets_frontend': [
            'nf_website_delivery_charge/static/src/js/web.js'
        ],
    },
    "images": ["static/description/background.gif", ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': False,
    "price": 60.99,
    "currency": "EUR"
}
