# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name" : "Down Payment For Purchase",
    "summary" : """
        odoo purchase down payment purchase advance payment vendor bill down payment purchase order down payment odoo purchase advance bill  purchase down payment percentage  purchase down payment fixed amount  vendor advance payment odoo purchase billing wizard odoo purchase bill automation  supplier advance payment odoo  purchase payment management odoo purchase customization down payment create bill vendor bill payment bill percentage fixed amount invoice purchase bill create purchase customer/vendor bill
    """,
    'post_init_hook': 'post_init_hook',
    "description" : """
        Create vendor bills with down payments directly from purchase orders. Support for percentage or fixed amount down payments with validation and automatic purchase order down payment line creation.
    """,
    "data" : [
        'security/ir.access.csv',
        'wizard/nf_purchase_advance_payment_bill.xml',
    ],
    "support": "nextflow@gmail.com",
    "author": 'NextFlowIT',
    "company": 'NextFlow Technology',
    "maintainer": 'NextFlow Technology',
    "website": 'https://www.nextflow.in',
    "version": "20.0.1",
    "depends" : ['purchase'],
    "license": 'OPL-1',
    "images": ["static/description/background.gif"],
    "price": 35.00,
    "installable" : True,
    "application": True,
    "auto_install": False,
    "currency": "EUR"
    
}
