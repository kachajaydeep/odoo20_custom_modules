# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

{
    'name': "Vehicle Rental Management",
    'author': 'NextFlowIT',
    'license': "OPL-1",
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'nextflow.in',
    'version': '20.0.1',
    'summary': """ car management car rent car rental  vehicle Odoo Vehicle Rental Management Vehicle Rental System Odoo Car Rental Management Odoo Fleet Rental Management Hourly Daily Monthly Vehicle Rental Odoo Rental Booking System Vehicle Rental Invoice Advance Payment Rental Odoo Multi Company Vehicle Rental Future Vehicle Booking Odoo Odoo vehicle booking vehicle rental booking system fleet booking management Odoo multi-company vehicle rental multi company fleet management hourly vehicle rental Odoo monthly car rental management flexible rental pricing rental order tax management Odoo rent order vehicle rental accounting rental history report Odoo vehicle rental analytics advance payment vehicle rental rental booking payment system vehicle rental invoice Odoo rental billing management future vehicle booking Odoo vehicle reservation system Odoo rental management odoo rent management car rental management vehicle rent management bike rent management truck rent management Rental product rental service rent product rent car rent machine rental machine rent Hire machinery Equipment Rental management machine rental real estate rental sales service Equipment rental property rent service rental Equipment Machinery rental service Odoo Rental Management for Machine Product and Equipements Fleet Rental management rental Fleet Management fleet rental   
    """,
    'post_init_hook': 'post_init_hook',
    'description': """
        Vehicle Rental Management for Odoo

        Vehicle Rental Management is a powerful and easy-to-use Odoo module designed to efficiently manage vehicle rentals for 
        businesses of all sizes. This app helps you streamline vehicle booking, rental orders, invoicing, payments, and 
        reporting-all from a single dashboard. With support for hourly, daily, and monthly rentals, it is ideal for car 
        rental agencies, transport companies, and fleet management businesses.
    """,
    'depends': ['account', 'product', 'fleet', 'base', 'delivery','mail'],
    'data': [
        'security/rental_security.xml',
        'security/ir.access.csv',
        'data/rental_cron.xml',
        'data/rental_sequence.xml',
        'data/vehicle_product_data.xml',
        'wizard/fleet_rent_advance_payment_view.xml',
        'reports/rental_reports.xml',
        'views/fleet_rent_line_views.xml',
        'views/fleet_rental_location_view.xml',
        'views/fleet_vehicle_inherit.xml',
        'views/res_partner_inherit.xml',
        'views/fleet_rent_views.xml',
    ],
    "images": ["static/description/background.gif"],
    'application': False,
    'installable': True,
    'auto_install': False,
    "price": 64.99,
    "currency": "USD"
}
