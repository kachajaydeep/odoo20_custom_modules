# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point of Sale Employee Access Rights for Restaurant",
    "summary": """ 
        pos access rights restrict user restrict users pos employee restriction empoyee access rights pos user access rights pos access right employee access hide edit plan hide button on restaurant hide disable buttons on pos restaurant point of sale restaurant hide create product hide create product on pos hide create product on point of sale restaurant disable create product on restaurant Hide Cancel Order Button Hide Split Button Hide Transfer/Merge Button Hide Create Product Hide Edit Plan Hide Switch Floor View Hide Payment Button Restrict Payment Method Hide Payment Tip Button Hide Ship Later Button Hide Payment Validate Button Hide Payment Invoice Button Hide Cash In/Out POS Button  Hide Delete Order Button Disable Price Button Disable Quantity Button Disable Discount Button Only Show Active Orders Hide Numpad Buttons Disable (+/-) Button Hide Refund Button Hide Info Button</l Hide Fiscal Button Hide Quotation Button Hide Pricelist Button Hide Close POS Button Hide Backend POS Button Hide POS Categories Hide Debug Window Hide Customer Button Hide Create Customer Button Hide Customer Note Button pos employee access rights cashier access rights pos restaurant access rights point of sale restaurant access rights waiter access rights kitchen screen rights pos restaurant restrictions access right management manage access rights pos restaurant access rights management 
        odoo pos employee rights odoo pos access control restaurant pos permissions odoo restaurant pos pos security pos role management hide pos buttons pos employee restrictions odoo restaurant access rights pos payment restriction hide refund button disable price button disable discount button pos cashier permissions restaurant pos control pos user permissions odoo pos restaurant module pos employee management odoo pos access rights restaurant employee permissions
        odoo pos access control odoo pos employee rights odoo restaurant pos restaurant pos permissions pos user permissions pos cashier permissions pos role management pos security pos employee management restaurant employee permissions odoo pos access rights hide pos buttons pos payment restriction hide refund button disable price editing disable discount button restaurant pos control odoo pos restaurant module
    """,
    "author": "NextFlowIT",
    "license": "OPL-1",
    "description": """ 
        Employee Access Rights for POS Restaurant 
        Control POS employee permissions in Odoo Restaurant. Hide buttons, restrict payments, refunds, discounts, customers, tables, orders, and POS actions securely.
    """,
    "category": "Point of sale",
    "website": "",
    "depends": ["nf_pos_employee_access_rights", "pos_restaurant"],
    "version": "20.0.1",
    "data": [
        "views/pos_employee.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_employee_access_rights_restaurant/static/src/overrides/control_buttons/control_buttons.xml",
            "nf_pos_employee_access_rights_restaurant/static/src/overrides/navbar/navbar.xml"
        ],
    },
    "images": [
        "static/description/background.gif",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": True,
    "price": 9.99,
    "auto_install": False,
    "currency": "EUR",
}
