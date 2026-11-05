# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

{
    "name" : "Employee Dashboard",
    "summary" : """
        employee dashboard odoo odoo hr dashboard employee dashboard module employee self service odoo odoo employee management employee attendance dashboard employee check in check out odoo employee break timing odoo odoo attendance management employee leave dashboard odoo employee expenses dashboard employee birthday reminder odoo employee anniversary dashboard company announcements odoo hr dashboard odoo 17 hr dashboard odoo 18 hr dashboard odoo 19 odoo hr employee portal employee management erp odoo odoo hrms dashboard attendance tracking odoo hr employee dashboard module nextflow technology odoo apps employee dashboard app for odoo odoo employee attendance system employee dashboard emp dashboard hr dashboard odoo employee dashboard employee attendance employee check in employee check out odoo hr management employee leave dashboard expenses dashboard employee birthday dashboard employee anniversary dashboard odoo employee portal module hr dashboard module odoo hr dashboard app employee announcements odoo hr dashboard for odoo erp
    """,
    "post_init_hook": 'post_init_hook',
    "description" : """
        Employee Dashboard for Odoo is a smart HR dashboard module that helps manage employee Leaves, Attendance, Expenses, Contracts, Birthdays, Anniversaries, Check-In, Check-Out, Break Timing, and Company Announcements with secure role-based access for Odoo 17, 18, and 19.
    """,
    "data" : [
        'security/nf_dashboard_security.xml',
        'security/ir.access.csv',
        'data/nf_announcement_data.xml',
        'views/nf_dashboard_announcement_views.xml',
        'views/nf_hr_employee_view.xml',
        'views/nf_dashboard_views.xml',
        'views/nf_action.xml',
        'views/nf_employee_management_view.xml',
        'views/nf_dashboard_menus.xml',
    ],
    "assets": {
        'web.assets_backend': [
            'nf_employee_dashboard/static/src/scss/nf_dashboard.scss',
            'nf_employee_dashboard/static/src/xml/nf_dashboard_templates.xml',
            'nf_employee_dashboard/static/src/js/nf_dashboard.js',
            'nf_employee_dashboard/static/src/scss/nf_employee_mangement.scss',
            'nf_employee_dashboard/static/src/xml/nf_employee_mangement.xml',
            'nf_employee_dashboard/static/src/js/nf_employee_management.js',
            'nf_employee_dashboard/static/src/xml/nf_timer_display.xml',
            'nf_employee_dashboard/static/src/js/nf_timer_display.js',
        ],
    },
    "support": "nextflow@gmail.com",
    "author": 'NextFlowIT',
    "company": 'NextFlow Technology',
    "maintainer": 'NextFlow Technology',
    "website": 'https://www.nextflow.in',
    "version": "20.0.1",
    "depends" : ['base', 'hr', 'hr_attendance', 'hr_holidays', 'hr_expense','web', 'contacts'],
    "license": 'OPL-1',
    "images": ["static/description/background.gif"],
    "installable" : True,
    "application": True,
    "auto_install": False,
    "price": 35.00,
    "currency": "USD"
    
}
