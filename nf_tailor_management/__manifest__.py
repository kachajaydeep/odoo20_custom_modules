# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Tailor Management System",
    'author' : 'NextFlowIT',
    "website": "",
    "support": "nextflow@gmail.com",
    "category": "manufacturing",
    "summary": "A comprehensive solution for managing tailoring services, from customer orders to invoicing and reporting. fabric management tailoring tailor management order tracking  inventory invoice management odoo tailor management module odoo tailor service management tailoring module odoo odoo custom clothing module odoo garment management system odoo tailor service app odoo fashion and tailoring management tailor shop odoo module odoo clothing alterations odoo tailoring management system odoo tailoring business module odoo stitching service management odoo garment industry management odoo tailor service customization tailor manufacturing ",
    "description": """ The Tailor Management System module for Odoo is designed to streamline the process of managing tailoring services within a business. This module allows businesses to efficiently handle customer orders, track fabric and material inventory, manage tailoring progress, and create invoices and reports. It integrates seamlessly with the Sales and Inventory modules, enabling smooth operations from customer order to final delivery.

        Key Features:
        - Manage customer orders with custom tailoring requirements
        - Track materials and fabric used for each order
        - Monitor tailoring progress and assign tasks to staff
        - Generate invoices and reports based on completed tailoring orders
        - Integrate with stock and sales management for accurate inventory tracking and order fulfillment  """,
    'post_init_hook': 'post_init_hook',
    "version": "20.0.1",
    'keywords': ['tailor management','fabric management',],
    "depends": ["base", 'contacts', 'sale_management', "mrp", 'stock', 'mail', 'spreadsheet'],
    "data": [
        'security/secutiry.xml',
        'security/ir.access.csv',
        'data/tailor_order_sequence.xml',
        'views/measurement/nf_measurement_line.xml',
        'views/measurement/nf_measurement.xml',
        'views/measurement/nf_measurement_type.xml',
        'views/measurement/nf_measurement_category.xml',
        'views/designs/design_type.xml',
        'views/designs/design_line.xml',
        'reports/tailor_eport.xml',
        'views/tailor_order.xml',
        'views/tailor_line.xml',
        'views/res_partners.xml',
        'views/sale_order.xml',
        'views/nf_actions.xml',
        'views/tailor_dashboad.xml',
        'views/nf_menus.xml',
        'views/res_configuration.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'nf_tailor_management/static/src/**/*'
        ],
    },
    "images": ["static/description/background.gif", ],
    "application": True,
    "auto_install": False,
    "installable": True,
    "price": 150.00,
    "currency": "EUR",
    "license": "OPL-1",
}

