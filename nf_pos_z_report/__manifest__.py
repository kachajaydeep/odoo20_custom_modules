# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "POS Z-Report",
    "version": "20.0.1",
    "summary": """  point of sale z report pos z report pos z-report point of sale z-report z reports z-reports x report pos z report day porfit los report session close report cashi in out report z report pos point of slae report pos report """,
    "description": """   point of sale z report pos z report pos z-report point of sale z-report z reports z-reports """,
    "category": "Point of sale",
    "website": "https://www.nextflow.in",
    "author": "NextFlowIT",
    "license": "OPL-1",
    "data": ["views/pos_session_view.xml", "reports/nf_pos_z_report_view.xml"],
    "depends": ["point_of_sale"],
    "images": [
        "static/description/background.gif",
    ],
    "post_init_hook": "post_init_hook",
    "price": 25.00,
    "installable": True,
    "application": True,
    "currency": "EUR",
}
