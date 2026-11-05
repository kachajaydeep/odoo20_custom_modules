# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

{
    "name":  "Product Catalog Generator",
    "summary" : """
        product catalog create odoo product catalog generator product catalog odoo odoo catalog report product catalog pdf odoo product catalog excel export odoo odoo product brochure generator dynamic product catalog odoo odoo product catalog printing odoo catalog report module product listing catalog odoo odoo catalog wizard odoo catalog styles odoo sales catalog generator odoo product catalog email send odoo catalog management module generate product catalog odoo automated product catalog odoo odoo product marketing catalog odoo report catalog module odoo printable product catalog product catalog product catalog generator catalog module erp catalog solution product catalog software catalog generator apps catalog module product catalog tool sales catalog generator product brochure generator Product Product Catalog Generator product catalog generator productcatalog catalog product
        """,
    'post_init_hook': 'post_init_hook',
    "description": """
        Create professional product catalogs directly in Odoo with the Product Catalog Generator module. Generate product or category-based catalogs with multiple styles, customizable layouts, pricing options, images, Excel export, PDF reports, and email sharing. Perfect for businesses needing dynamic product brochures and sales catalogs.
    """,
    "data": [
        "security/catalog_groups.xml",
        "security/ir.access.csv",
        "data/actions.xml",
        "data/email_template.xml",
        "reports/catalog_report_template_style_01.xml",
        "reports/catalog_report_template_style_02.xml",
        "reports/catalog_report_template_style_03.xml",
        "reports/catalog_report_template_style_04.xml",
        "reports/catalog_report_template_style_05.xml",
        "reports/reports.xml",
        "views/nf_product_catalog.xml",
        "wizard/nf_generate_product_catalog.xml",
    ],        
    "support": "nextflow@gmail.com",
    "author": 'NextFlowIT',
    "company": 'NextFlow Technology',
    "maintainer": 'NextFlow Technology',
    "website": 'https://www.nextflow.in',
    "version": "20.0.1",
    "depends": ["product"],
    "license": 'OPL-1',
    "images": ["static/description/background.gif"],
    "installable" : True,
    "application": True,
    "auto_install": False,
    "price": 59.00,
    "currency": "USD"
} 