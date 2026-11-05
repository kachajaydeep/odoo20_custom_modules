# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

{
    "name": "Create Purchase Order from POS | Odoo POS Purchase Integration",
    "summary": """create po from pos create po from point of sale purchase order from pos purchase order from point of sale pos purchase order pos po pos po receipt pos po bill pos po validate receipt pos po create bill pos purchase order receipt pos purchase order bill purchase from pos purchase from point of sale restaurant pos purchase bar pos purchase po from pos restaurant po from pos bar purchase order management from pos purchase order management point of sale pos purchase order management purchase order management pos module purchase order management from point of sale module create purchase from pos create purchase from point of sale generate purchase order from pos convert purchase from pos purchase order create sale odoo create po from pos pos purchase order integration generate purchase order from pos odoo pos purchase management purchase order automation in pos pos purchase integration pos inventory replenishment pos supplier order creation pos auto purchase order pos reorder management pos stock refill from supplier purchase workflow in pos purchase management from pos how to create purchase order from pos in odoo auto generate purchase order from pos pos purchase order automation app odoo pos purchase order integration streamline purchasing from pos transactions automatic vendor purchase from pos sales purchase order creation flow from point of sale save time with auto po generation seamless pos to purchase workflow manage supplier orders from pos improve stock management with auto purchase odoo pos integrated purchasing pos purchase management pos reorder automation purchase integration auto po from pos pos purchase order app odoo pos extension purchase management pos management point of sale management stock management inventory management supplier management vendor management order management business automation retail management restaurant management wholesale management franchise management""",
    "post_init_hook": "post_init_hook",
    "description": """
    Create Purchase Order from POS | Odoo POS Purchase Integration
    
    Overview
Easily create purchase orders from POS in Odoo with this smart extension. Whenever you make a sale in Point of Sale, the system can generate a corresponding Purchase Order to restock inventory or fulfill customer demand — ensuring your stock never runs out.
This app is ideal for businesses looking to automate reordering, streamline procurement, and connect POS sales to supplier purchasing — all within a single click.

    🔹 Key Features
🔄 Auto-create Purchase Orders directly from POS orders
🏪 Seamless Integration between POS and Purchase Management
🧾 Customizable Rules for product, supplier, and quantities
📦 Stock Replenishment made simple from POS sales
📋 Vendor Mapping for accurate supplier order generation
⚙️ Supports Odoo 18 Community & Enterprise

    Benefits
Eliminate manual purchase entry
Maintain optimal stock levels automatically
Improve supplier communication and accuracy
Save time and reduce human error
Create a smooth POS to Purchase workflow

    🔍 Use Cases
Retail stores generating supplier orders after sales
Restaurants restocking ingredients from POS sales
Wholesale businesses managing dynamic inventory
Franchise stores syncing sales with purchase orders
    """,
    "category": "Purchase/Point of Sale",
    "author": "NextFlowIT",
    "license": "OPL-1",
    "company": "NextFlow Technology",
    "maintainer": "NextFlow Technology",
    "website": "nextflow.in",
    "version": "20.0.1",
    "depends": ["point_of_sale", "purchase_stock", "pos_hr"],
    "data": [
        "views/pos_config.xml",
        "views/purchase_order.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_purchase_order/static/src/**/*"
        ]
    },
    
    "images": [
        "static/description/background.gif"
    ],
    
    "application": True,
    "installable": True,
    "auto_install": False,
    "price": 24.99,
    "currency": "USD",
}