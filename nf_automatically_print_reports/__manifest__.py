# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.
{
    "name": "Automatically Print Reports",
    "summary": """ Automatically Print Reports  batch print invoices PDF generator bulk print sales orders vendor bill PDF print quotes  automated reports   ERP productivity  print automation download multiple invoices   report management automatic print pos reports pos report print sale report print sale reports print auto print report automat print report report print direct print report direct print pdf auto print pdf report """,
    "post_init_hook": "post_init_hook",
    "description": """Stop manual printing. Bulk select sales orders, vendor bills, and quotes to generate PDFs in one click. The fastest  print automation module for high-volume ERP workflows.""",
    "version": "20.0.1",
    "depends": ["base", "base_setup"],
    "data": [
        "views/res_config_settings_view.xml",
    ],
    "author": "NextFlowIT",
    "company": "NextFlow Technology",
    "maintainer": "NextFlow Technology",
    "website": "https://www.nextflow.in",
    "assets": {
        "web.assets_backend": [
            "nf_automatically_print_reports/static/src/overrides/action_service.js",
            "nf_automatically_print_reports/static/src/overrides/print.min.js",
        ],
    },
    "license": "OPL-1",
    "images": ["static/description/background.gif"],
    "application": False,
    "installable": True,
    "auto_install": False,
    "price": 80.60,
    "currency": "EUR",
}
