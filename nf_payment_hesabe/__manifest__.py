# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': "Payment Provider Hesabe",
    'summary': """
        payment provider hesabe hesabe payment provider odoo hesabe payment gateway hesabe payment integration odoo payment provider hesabe odoo integration online payment gateway odoo odoo payment acquirer hesabe payment module odoo ecommerce payment gateway secure online payments odoo hesabe api integration odoo website payment gateway hesabe checkout integration odoo online payment solution payment gateway for odoo hesabe payment processing odoo invoice payment gateway accept online payments odoo hesabe payment services odoo accounting payment integration hesabe merchant integration odoo website checkout payment middle east payment gateway kuwait payment gateway gcc payment gateway online transaction processing odoo odoo payment automation hesabe payment configuration odoo ecommerce checkout hesabe payment api odoo customer payment portal digital payment solution odoo odoo subscription payments hesabe secure payments odoo financial integration website payment collection odoo odoo online invoice payment hesabe ecommerce integration odoo website payments payment gateway customization odoo payment connector online billing odoo odoo checkout integration payment management odoo odoo payment processing ecommerce payment solution business payment automation odoo payment module nextflow technology odoo module 
        Payment acquire Hesabe payment hesabe website Hesabe Payment website hesabe payment hesabe website payment website payment provider ecommerce hesabe payment acquire ecommerce hesabe payment provider Hesabe Payment Gateway Odoo Hesabe Integration Odoo Payment Provider Online Payment Gateway Odoo eCommerce Payment Secure Online Payments Invoice Online Payment Website Checkout Payment Payment Acquirer Odoo Hesabe API Integration Odoo Accounting Payment Digital Payment Solution Odoo Payment Integration Middle East Payment Gateway Odoo eCommerce Hesabe Kuwait Hesabe Odoo payment Hesabe payment gateway Odoo Odoo Hesabe integration Hesabe payment provider Odoo online payment Hesabe Hesabe Kuwait payment gateway Odoo payment gateway Kuwait Hesabe API Odoo Odoo eCommerce Hesabe Odoo website payment Hesabe Hesabe credit card payment Odoo Odoo checkout Hesabe Odoo payment acquirer Hesabe Hesabe redirect payment Odoo Odoo ERP Hesabe integration hesabe implementation
    """,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'description': """
        Hesabe Payment Provider for Odoo integrates the Hesabe payment gateway with Odoo, enabling secure and reliable online payments for Odoo websites and eCommerce platforms.

        This module allows businesses, especially in Kuwait and the GCC region, to accept payments via Hesabe directly from Odoo checkout pages. It supports smooth redirection to Hesabe, secure transaction processing, and automatic payment status updates within Odoo.

        Key Features:
        Seamless Hesabe payment gateway integration with Odoo
        Secure online payments for Odoo Website & eCommerce
        Automatic payment confirmation and transaction tracking
        Easy configuration using Hesabe API credentials
        Compatible with Odoo's standard payment workflow
        Ideal for businesses using Hesabe in Kuwait and GCC

        This module is perfect for merchants looking to offer trusted Hesabe payment options to their customers while maintaining full control inside Odoo.
    """,
    'category': 'Accounting/Payment Providers',
    'author': 'NextFlowIT',
    'license': "OPL-1",
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'nextflow.in',
    'version': '20.0.1',
    'depends': ['payment'],
    'external_dependencies': {
        'python': ['pycryptodome'],
        # 'apt': {
        #     'pycryptodome': 'python3-pycryptodome',
        # },
    },
    'data': [
        'views/payment_hesabe_template.xml',
        'views/payment_views.xml',
        'data/payment_provider_data.xml',
        'data/payment_method_data.xml',
    ],
    "images": ["static/description/background.gif"],
    'application': True,
    'installable': True,
    'auto_install': False,
    "price": 99.99,
    "currency": "USD"
}
