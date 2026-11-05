# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

{
    'name': "Attendance from pos",
    'summary': """
        point of sale employee attendance odoo pos attendance pos employee attendance odoo check in check out odoo employee login pos workforce management odoo attendance tracking employee time tracking pos time management odoo work hours calculation odoo attendance reports odoo employee authentication pos staff management odoo location tracking odoo employee check in odoo attendance dashboard odoo hr attendance pos odoo resource attendance odoo employee monitoring odoo pos workforce tracking odoo attendance module
        manage attendance from pos attendance from pos check in from pos checkout from pos check-in from pos check-in pos check-out from pos check-out pos employee attendance pos employee attendance pos check-in check-check-out check in check out fro pos attendance pos employee attendance 
    """,
    'post_init_hook': 'post_init_hook',
    'description' : """
        Manage employee attendance with secure login, check-in and check-out functionality, employee authentication, role-based access control, attendance tracking, and comprehensive daily, weekly, and monthly attendance reports directly within Odoo.
    """,
    'data': [
        'data/hr_notification.xml',
        'views/res_pos_config.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_pos_employee_attendance/static/src/overrides/**/*',
        ],
    },
    'version': "20.0.1",
    'category': 'Sales/Point of Sale',
    'depends': ['point_of_sale', 'hr_attendance', 'pos_hr'],
    'license': "OPL-1",
    'website': '',
    'author' : 'NextFlowIT',
    'images': ["static/description/background.gif" ],
    'auto_install': False,
    'installable': True,
    'application' : True,
    'live_test_url': 'https://youtu.be/MMYMIblEqw4',
    'price': 20.10,
    'currency': "EUR"
}
