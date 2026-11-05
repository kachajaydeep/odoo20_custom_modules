# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name" : "Sale Auto Workflow",
    "summary": """
        odoo sale auto workflow one click sale odoo  odoo sales automation  auto confirm sale order odoo auto validate delivery odoo  auto create invoice odoo  auto register payment odoo  odoo automatic sales process  odoo sales workflow automation  sale order automation odoo  automatic invoicing odoo  odoo sales process automation  odoo one click workflow odoo sales order automation odoo auto payment invoice validate payment create invoice create sale order one click create button sale order create
    """,
    # 'post_init_hook': 'post_init_hook',
    "description": """
        Automate the entire Odoo sales process with the Sale Auto Workflow module. Use the One Click Sale button to automatically confirm sale orders, validate deliveries, create invoices, and register payments with configurable workflow settings.
    """,
    "data": [
        'views/nf_sale_order_view.xml',
        'views/nf_res_config_setting_view.xml',
    ],
    "support": "nextflow@gmail.com",
    "author": 'NextFlowIT',
    "company": 'NextFlow Technology',
    "maintainer": 'NextFlow Technology',
    "website": 'https://www.nextflow.in',
    "version": "0.0.2",
    "depends": ['sale_management', 'stock', 'account'],
    "license": 'OPL-1',
    "images": ["static/description/background.gif"],
    "installable" : True,
    "application": True,
    "auto_install": False,
    "price": 15,
    "currency": "USD"


}