# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Point Of Sale Employee Access Rights",
    "summary": """pos access rights restrict user restrict users pos employee restriction empoyee access rights pos user access rights Hide Payment Button Restrict Payment Method Hide Payment Tip Button Hide Ship Later Button Hide Payment Validate Button Hide Payment Invoice Button Hide Cash In/Out POS Button  Hide Delete Order Button Disable Price Button Disable Quantity Button Disable Discount Button Only Show Active Orders Hide Numpad Buttons Disable Button Hide Refund Button Hide Info Button Hide Fiscal Button Hide Quotation Button Hide Pricelist Button Hide Close POS Button Hide Backend POS Button Hide POS Categories Hide Debug Window Hide Customer Button Hide Create Customer Button Hide Customer Note Button pos employee access rights restrict employee access rights for employee pos access rights pos restrictions restrict pos record rule for pos pos user rights pos cashier access rights point of sale employee point of sale cashier restrict pos cashier rightspos employee access rights 
        pos user permissions pos role management pos security pos restrictions hide pos buttons disable pos price disable pos discount pos access control odoo pos employee rights pos button visibility pos user restrictions odoo point of sale security pos workflow control odoo pos permissions retail pos management pos employee roles odoo pos customization pos interface control pos security module point of sale employee access rights pos employee access rights odoo pos employee permissions odoo pos access control pos user access pos role management pos security pos button restrictions pos employee restrictions odoo point of sale hide pos buttons
        pos user permissions pos employee roles odoo pos customization retail pos security odoo pos employee access rights odoo pos user permissions pos access control module pos role based access control pos employee security restrict pos actions disable price button pos disable discount button pos hide payment button pos hide refund button pos hide customer button pos restrict payment methods odoo pos hide cash in out pos hide pos categories hide numpad buttons odoo pos security module odoo pos employee restrictions point of sale role management odoo pos workflow control pos interface customization multi employee pos access odoo pos permissions module pos access right """,
    "author": "NextFlowIT",
    "license": "OPL-1",
    "description": """ employee access rights.
        Control employee access in Odoo POS with role-based permissions. Hide buttons, restrict payments, disable discounts, refunds, price edits, and secure POS operations.
    """,
    "category": "Point of sale",
    "website": "",
    "depends": ["point_of_sale", "pos_hr","pos_stock", "pos_sale"],
    "version": "20.0.2",
    "data": ["views/pos_employee.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_employee_access_rights/static/src/overrides/**/*"
        ],
    },
    "images": [
        "static/description/background.gif",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": True,
    "price": 25.42,
    "auto_install": False,
    "currency": "EUR",
}
