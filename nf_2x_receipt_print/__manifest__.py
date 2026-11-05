# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

{
    "name": "Point of sale 2x Print",
    "summary": """receipt 2x kitchen receipt 2x receipt 2x pos receipt Odoo POS POS 2x Print Dual Receipt Print POS Double Receipt Point of Sale Receipt Copy Odoo Point of Sale Printing POS Multi Printer Odoo POS Custom Receipt Odoo POS Print Twice Customer and Internal Receipt Kitchen Receipt Print Odoo POS Automation POS Print Module Odoo POS Addon Odoo 17 POS Extension POS Receipt Template Odoo POS Invoice Print POS Multiple Copies POS Two Receipts POS Receipt Automation Odoo POS Enhancement  Upgrade your Odoo POS experience with the Point of Sale 2x Print module today, and streamline your receipt printing process. Download now from the Odoo App Store dual print receipt 2x print 2x print receipt many print receipt print many more multiple print multi print receipt pos many receipt pos 2x print receipt kitchen receipt 2x kitchen receipt 2x receipt 2x pos receipt multi pos receipt print multiple pos receipt pos auto receipt print odoo pos 2x print Multiple receipt printing point of sale Multiple print odoo pos printer multiple receipt printing pos multi printer customer receipt internal receipt kitchen receipt warehouse receipt odoo retail module odoo point of sale receipt customization automatic receipt printing pos receipt duplicate odoo apps Odoo Point of Sale pos 2x Print multiple printers retail invoice printing receipt printing Odoo POS POS system Odoo module POS enhancements printing solutions hospitality pos 2x print pos 2x receipt pos receipt pos 2x receipt pos order print oderline print""",
    "author": "NextFlowIT",
    "license": "OPL-1",
    "description": """Point of Sale 2x Print
        ======================
        This module extends the standard Odoo Point of Sale workflow by offering **automatic dual receipt printing**. 
        After payment, two receipts are produced — one for the customer and another for internal or auxiliary use 
        (e.g., kitchen, warehouse, or administrative records).

        **Key Features:**
        -----------------
        - Automatic dual printing: generates two copies of a receipt in one transaction.  
        - Separate customization for each copy (e.g., detailed vs simplified).  
        - Multi-printer support: send the second copy to a different printer.  
        - Flexible print timing: immediately after payment or configurable delay.  
        - Seamless integration into POS flow without performance impact.  

        **Technical Details:**
        ----------------------
        - Compatibility: Odoo 17.0+  
        - Dependencies: `point_of_sale`, `mail`, `stock`, `account`  
        - License: OPL-1  
        - Note: Not supported in offline POS mode.  

        **Use Case:**
        -------------
        If your business needs printed copies of POS transactions for multiple departments (customer, kitchen, 
        warehouse, or accounting), this module automates that process and avoids manual duplication — improving speed, 
        accuracy, and consistency.

        **Setup Steps:**
        ----------------
        1. Install the module.  
        2. Configure printers in POS settings (primary and secondary).  
        3. Customize the layout for each receipt copy.  
        4. Choose automatic or manual print mode for the second receipt.  
        5. Start POS sessions — dual-printing will activate automatically.

        **Support & Customization:**
        ----------------------------
        Free support for 90 days after purchase.  
        Customizations available on request via the vendor's contact information.
   """,
    "category": "Poiunt of sale",
    "website": "nextflow.in",
    "depends": ["point_of_sale"],
    "version": "20.0.1",
    "data": ["views/res_pos_config.xml"],
    "support": "nextflowit@gmail.com",
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_2x_receipt_print/static/src/override/models.js"
        ],
    },
    'images': ['static/description/background.gif'],
    'post_init_hook': 'post_init_hook',
    "price":18.40,
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR",
}