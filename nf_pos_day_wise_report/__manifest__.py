# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.
{
    "name": "POS Day Wise Report",
    "author": "NextFlowIT",
    "license": "OPL-1",
    "summary": """Point Of Sale day wise report pos day wise report pos report report day wise employee report pos employee report daily report day report user day report user report day report user day wise report day vise report day sale report pos sale report full day report full day sale report pos full day report pos day report z report 
        odoo pos report pos day wise report odoo pos day wise report pos user wise report pos employee wise report odoo pos user report odoo pos employee report point of sale report odoo pos sales report pos daily report pos user wise sales pos employee wise sales odoo point of sale pos reporting odoo pos reporting daily pos sales report pos analysis report pos day wise report pos daily report pos user wise report pos employee wise report odoo pos reporting odoo pos sales report odoo point of sale report pos user report pos employee report daily pos analysis pos sales analysis pos management report
    """,
    "post_init_hook": "post_init_hook",
    "description": """  Pos Day Wise Report
        Generate and print day-wise Odoo POS reports based on users, employees, or both. Analyze daily POS activity with flexible user-wise and employee-wise reporting.
    """,
    "category": "Point of sale",
    "website": "",
    "version": "20.0.1",
    "depends": ["point_of_sale", "pos_hr"],
    "data": [
        "security/ir.access.csv",
        "report/report_pos_day_wise.xml",
        "wizard/pos_day_wise_report_wizard_views.xml",
    ],
    "images": [
        "static/description/background.gif",
    ],
    "price": 21.42,
    "application": True,
    "installable": True,
    "auto_install": False,
    "currency": "EUR",
}
