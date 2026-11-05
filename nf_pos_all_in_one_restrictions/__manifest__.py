# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'All in one Sale Restriction || Pos Sale Restriction || Transfer restriction',
    'summary': """
        Odoo Sale Restriction | Odoo POS Sale Restriction | Odoo POS Stock Info | Odoo POS Stock Quantity | Odoo Stock Restriction | Odoo Out of Stock Restriction | Odoo Inventory Restriction | Odoo Stock Warning | Odoo POS Stock Warning Odoo Sale Order Stock Restriction Odoo Internal Transfer Restriction Odoo Stock Availability Odoo On Hand Quantity POS Odoo Warehouse Stock POS Odoo Location Stock POS Odoo Prevent Negative Stock Odoo Prevent Overselling Odoo Inventory Management Odoo Multi Warehouse Stock Odoo POS Inventory Odoo Stock Control Odoo Product Stock Warning
        all in one sale restriction pos sale restriction transfer restriction odoo sale restriction odoo pos restriction odoo stock transfer restriction sales order restriction point of sale restriction inventory transfer restriction stock validation restriction odoo inventory control odoo stock restriction restrict sale order creation restrict pos order creation restrict internal transfer insufficient stock restriction stock availability validation odoo warehouse restriction sales and inventory control odoo stock management  prevent overselling odoonegative stock restriction  inventory validation modulestock control system odoo sales management odoo pos management warehouse transfer control product stock validation odoo business automation nextflow technology odoo module 
        point of sale restrict sale if stock is low or don't have enough stock all in one restriction Restrict Stock Transfer restrict stock transfer restrict internal transfer create so restriction out of stock restriction out out of stock so restriction stock authentication so authentication sale order authentication pos restrict low stock restrict create pos order out of stock restriction inventory restriction pos warehpuse quantity display warehpuse qty display stock in pos display stock point of sale display stock pos restriction so po restrict transfer restrict full restrict order restriction 
        """,
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'post_init_hook': 'post_init_hook',
    'description': """ Restrict to create so if then stock is low. 
        If on hand stock is low and try to create so more than on hand qty one warning is raise for low stock. 
        Prevent out-of-stock Sale Orders, POS sales and internal transfers in Odoo. Display On Hand stock, warehouse quantities and stock warnings directly in POS.
        """,
    'category': "",
    'website': 'nextflow.in',
    'depends': ['sale_management', 'stock', 'nf_restrict_so', 'nf_restrict_transfer', 'nf_pos_sale_restriction'],
    'version': '20.0.1',
    "images": ["static/description/background.gif", ],
    "price": 5.00,
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR"
}
