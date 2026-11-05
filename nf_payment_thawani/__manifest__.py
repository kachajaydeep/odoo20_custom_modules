# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': "Payment Provider Thawani",
    'category': 'Accounting/Payment Providers',
    'author': 'NextFlowIT',
    'license': "OPL-1",
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'nextflow.in',
    'version': '20.0.1',
    'summary': """
    Payment Provider:
        payment provider thawani thawani payment gateway odoo thawani payment integration odoo thawani payment provider odoo payment gatewaythawani checkout integration online payments with thawani odoo ecommerce payment gateway thawani payment module odoo thawani integration 
        Thawani Payment Gateway integration for odoo Online Payment Thawani payment integration, Thawani checkout integration, Thawani account login, Thawani Secure online payments, Thawani transaction, Thawani pay, E-commerce Payment Invoice Payment Debit Card Payment Credit Card Payment Omani rial OMR Oman Payment Thawani Payment Gateway | Odoo Thawani Payment | Odoo thawani integration | Payment thawani | Odoo thawani payment gateway | Tokenization | Save card | Odoo Thawani Checkout Payment | Multiple Currencies | 3D Secure | Fast checkout | Multi-currency Support Odoo Thawani Checkout Payment ensures safe and quick payments. It includes 3D Secure, easy refunds, and support for different currencies Users can now save cards and pay instantly using just CVV OTP Website Thawani Checkout Payment Acquirer Thawani Odoo payment gateway, Odoo Thawani integration, Odoo payment gateway Oman, Odoo ecommerce payment, Thawani payment Odoo module, Odoo invoice online payment, Odoo portal payment, Oman payment gateway ERP Thawani Odoo payment gateway Thawani payment gateway Odoo Odoo Thawani integration Thawani payment Odoo module Odoo online payment Thawani Odoo payment gateway Oman Oman payment gateway Odoo Odoo ecommerce payment gateway Odoo invoice payment gateway Odoo portal invoice payment Odoo website payment integration Odoo checkout payment gateway Thawani payment gateway integration for Odoo How to integrate Thawani in Odoo Odoo ecommerce Thawani payment Pay invoices online using Thawani in Odoo Thawani payment for Odoo customer portal Secure online payments in Odoo using Thawani Odoo payment acquirer Thawani Odoo payment provider Thawani Odoo ERP online payment gateway Odoo sales payment integration Odoo accounting payment gateway Oman online payment gateway Odoo Thawani Oman payment gateway Odoo Middle East payment gateway Odoo
        بوابة دفع ثواني أودو
        ثواني بوابة دفع أودو
        تكامل ثواني مع أودو
        بوابة الدفع ثواني في أودو
        الدفع الإلكتروني ثواني أودو
        بوابة دفع أودو في عمان
        بوابة الدفع الإلكتروني أودو
        الدفع الإلكتروني لمتجر أودو
        الدفع عبر الفواتير في أودو
        دفع فواتير أودو أونلاين
        بوابة دفع لموقع أودو
        تكامل بوابة الدفع ثواني مع نظام أودو
        كيفية ربط ثواني مع أودو
        الدفع الإلكتروني للمتاجر باستخدام أودو وثواني
        سداد الفواتير عبر بوابة ثواني في أودو
        بوابة دفع ثواني لمتجر أودو الإلكتروني
        الدفع الآمن عبر الإنترنت باستخدام أودو وثواني
        موفر الدفع ثواني أودو
        مزود الدفع ثواني في أودو
        وحدة الدفع الإلكتروني ثواني أودو
        نظام تخطيط الموارد أودو بوابة دفع
        بوابة الدفع ثواني في سلطنة عمان
        بوابة دفع عمان أودو
        الدفع الإلكتروني في عمان أودو
        ثواني بوابة الدفع العمانية أودو
        بوابة دفع ثواني أودو, تكامل ثواني مع أودو, الدفع الإلكتروني أودو,
        بوابة دفع أودو عمان, دفع فواتير أودو أونلاين, متجر أودو الإلكتروني,
        ثواني بوابة الدفع عمان
    """,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'description': """
        This module allows seamless integration of the Thawani Payment Gateway with Odoo ERP, enabling secure and reliable online payments for Odoo eCommerce and Customer Portal invoice payments.
        Customers can easily pay using Thawani directly from the Odoo website checkout page or from their portal invoices.

        The app supports real-time payment processing, automatic payment status updates, and smooth redirection after successful or failed transactions. It is ideal for businesses in Oman looking to accept online payments through Thawani while managing sales and accounting within Odoo.

        Key Features:
        Thawani payment gateway integration with Odoo
        Pay invoices from the Odoo customer portal
        Secure online payments for Odoo eCommerce
        Automatic payment confirmation and order validation
        Easy configuration from Odoo backend
        Supports multiple currencies (as per Thawani settings)
    """,
    'depends': ['payment','payment_authorize'],
    'data': [
        'views/payment_thawani_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
    ],
    "images": ["static/description/background.gif"],
    'application': False,
    'installable': True,
    'auto_install': False,
    "price": 99.99,
    "currency": "USD"
}
