# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': "Quick Purchase Order line",
    'summary': ''' 
        quick purchase order line odoo quick purchase order line quick add product in purchase order odoo purchase order fast entry purchase order line management odoo purchase automation odoo purchasing productivity quick product selection odoo odoo purchase efficiency module odoo purchase order improvement odoo purchase customization odoo apps purchase module purchase order line quick add odoo procurement management odoo purchasing workflow optimization odoo business automation odoo purchase order enhancement fast purchase order creation odoo vendor purchase management nextflow technology odoo module
        purchase order line quick order line quick purchase order line add order line quick quick add order line quick add purchase order line quick line line add orderline quick po line po lines purchase order lines direct po line direct add line add purchase order line quick ol create po line create po 
        odoo purchase order odoo purchase order line quick purchase order odoo purchase purchase order product add product purchase order odoo product odoo product creation edit product odoo purchase order management odoo purchase management direct add product quick purchase order line product purchase product add product fast add fast product add quick product add quick purchase order
    ''',
    'post_init_hook': 'post_init_hook',
    'description': """
        Quickly add products to Purchase Order lines in Odoo with a faster and more efficient entry process. This app helps reduce unnecessary clicks, improve purchasing productivity, and streamline Purchase Order creation.
        Add products directly to Odoo Purchase Order lines without clicking "Add Product." You can also create new products or edit existing products directly from the order line, making product management faster and more convenient.
        Simplify your purchasing workflow, reduce repetitive actions, and create Purchase Orders more efficiently with quick product selection and easy order line management.
    """,
    'data': [ 
        'views/nf_purchase_ordelrine.xml'
    ],
    'author': 'NextFlowIT',
    'license': "OPL-1",
    'category': "Purchase",
    'website': 'nextflow.in',
    'depends': ['base','purchase'],
    'version': '20.0.1',
    'images': ["static/description/background.gif"],
    'price': 10.00,
    'installable': True,
    'application': True,
    'auto_install': False,
    'currency': "EUR"
}
