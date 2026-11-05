# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Sale Boxes On Website',
    'summary': """
        odoo website box sales odoo product box quantity odoo sell products in boxes odoo ecommerce box products odoo website box packaging odoo product box size odoo website optional products odoo website add to cart optional product odoo box quantity calculator odoo product packaging website odoo website product quantity management odoo box order management odoo website sales enhancement odoo ecommerce quantity calculation odoo product packaging sales odoo website product boxes odoo online store box products odoo sales box quantity odoo product box selection odoo website product packaging prodcut box optional product options product website optional product product optional website prodcut options website product optional ecommerce product optional sweet saling with box ecommerce box sale e-commerce box sale
    """,
    'post_init_hook': 'post_init_hook',
    'description': """ 
        Sell products in predefined box quantities on your Odoo website. Allow customers to purchase products by box size, automatically calculate quantities and pricing, display optional boxed products during add-to-cart, and seamlessly integrate with Odoo eCommerce and Sales modules without any coding.
    """,
    'data': [
        'views/product.xml'
     ],
    'assets': {
       'web.assets_frontend': [
            'nf_website_boxes/static/src/js/configurationpopup/*'
        ],
    },
    'images': ["static/description/background.gif" ],
    'category': "Website/Website",
    'website': 'nextflow.in',
    'depends': ['website_sale'],
    'version': '20.0.1',
    'author': 'NextFlowIT',
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
    "price": 56.42,
    "currency": "EUR"
}
