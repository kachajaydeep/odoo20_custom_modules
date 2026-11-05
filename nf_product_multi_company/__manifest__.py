# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.
{
    "name": "Product Multi Company",
    'summary': """odoo multi company product management odoo product company access control multi company module odoo product variant company restriction odoo odoo multi company manager company wise product visibility odoo odoo access control products odoo multi company security module product multi company access odoo odoo company switch product module multi company product multi company product variant multi company multi company access right manager and user base multi company""",
    'post_init_hook': 'post_init_hook',
    'description': """Manage products and product variants across multiple companies in Odoo with ease. This module enables role-based access control, secure company-wise product visibility, and seamless switching between companies, ensuring proper multi-company data separation and improved security.""",
    "version":"20.0.1",
    "data":[
        'security/ir.access.csv',
        'security/nf_multi_company_access_rule.xml',
        'security/ir_rule.xml',
        'views/product_template.xml',
        'wizard/nf_website_update_wizard_views.xml',
        'data/website_update_wizard_view.xml',
    ],
    'author': 'NextFlowIT',
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'https://www.nextflow.in',
    "depends":['base', 'product'],
    "images": ["static/description/background.gif"],
    "license":'OPL-1',
    'application': True,
    'installable': True,
    'auto_install': False,
    "price": 15.50,
    "currency": "USD"
}