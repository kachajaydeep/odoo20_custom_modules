# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name" : 'Multi Barcode',
    "version" : '20.0.1',
    'summary': ''' multi barcode module for odoo, odoo multi barcode customization, odoo multiple barcode support, odoo barcode module development, custom barcode module in odoo, odoo product multiple barcode module, odoo multi barcode per product, odoo barcode customization service, odoo barcode scanning module, odoo inventory barcode customization, odoo warehouse barcode solution, odoo pos multi barcode module, odoo erp barcode integration, odoo barcode management system, custom odoo barcode solution, odoo product barcode mapping, odoo sku and barcode support, odoo variant barcode module, odoo serial number barcode, odoo batch barcode system, odoo qr code and barcode module, odoo stock barcode scanning, odoo logistics barcode module, odoo module development company, odoo customization services, odoo erp development india, odoo technical partner, odoo barcode module provider, hire odoo developer for barcode module, product multi barcode ''',
    'description': """ multi barcode module for Odoo that allows assigning multiple barcodes to a single product. supports barcode scanning in inventory, pos, and warehouse operations, improves product identification, reduces manual errors, and ensures seamless integration with existing odoo barcode and stock management features. """,
    "depends" : ['sale_management', 'product', 'stock', 'purchase'],
    'post_init_hook': 'post_init_hook',
    "data"  : [
        'security/ir.access.csv',
        'views/nf_res_config_setting_view.xml',
        'views/nf_product_product_view.xml',
        'views/nf_product_template_view.xml',
    ],
    'category': 'Sales',
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'https://nextflow.in',
    "images": ["static/description/background.gif"],
    "price": 24.59,
    'live_test_ur': '',
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR"
}
