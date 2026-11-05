# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "Create Sale Order From Point of sale",
    "summary": """ 
        create sale order from pos generate so so_from_pos saleorder pos create sale order pos creation pos create so from po sale order pos order label point of sale order label order lable pos lable receipt order  cart label pos order section section pos section sale from pos pos to sale create so from pos sale order creation 
        odoo create sale order from pos odoo pos sale order odoo quotation from pos odoo point of sale quotation odoo pos to sale order odoo pos sales order odoo pos quotation odoo offline pos odoo pos section line odoo sales management odoo retail odoo point of sale customization odoo pos extension sale create pos create sale order pos sale order create pos pos quotation order pos sale order odoo create sale order from pos odoo create quotation from pos odoo pos sale order odoo pos quotation odoo point of sale sale order odoo point of sale quotation odoo pos to sale order odoo pos to quotation odoo create sales order from point of sale odoo quotation from point of sale odoo pos order to sale order odoo pos order to quotation odoo sale order from pos odoo quotation from pos order odoo sales management odoo point of sale odoo pos customization odoo pos extension odoo retail management odoo retail pos odoo offline pos odoo offline point of sale odoo pos offline mode receipt print odoo pos receipt printing odoo section in sale order odoo section in quotation odoo section in pos order odoo order section odoo sale order section odoo quotation section odoo pos section line odoo clickable sale order odoo sale order popup odoo quotation popup odoo pos confirmation popup odoo sale order link odoo one click sale order odoo one click quotation odoo quick sale order odoo quick quotation odoo sales workflow odoo sales automation odoo point of sale workflow odoo customer quotation odoo retail sales odoo sales order management odoo pos integration pos sale order quotation from pos
    """,
    "author": "NextFlowIT",
    "license": "OPL-1",
    "description": """ 
        This App is use to create sale order form pos, This app add functionality in you system to genereate sale order from pos 
        Create Quotation and Sale Order directly from Odoo Point of Sale. One-click POS to Sale Order conversion, section support, offline compatible, and easy sales workflow.
        """,
    "post_init_hook": "post_init_hook",
    "category": "Point of sale",
    "website": "",
    "depends": ["point_of_sale", "sale_management"],
    "version": "20.0.1",
    "data": [
        "data/data.xml",
        "views/nf_config_pos.xml",
        "views/nf_res_config_settings_view.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_create_saleorder/static/src/app/buttons/*",
            "nf_pos_create_saleorder/static/src/app/popups/*",
            "nf_pos_create_saleorder/static/src/models/nf_create_saleorder_model.js",
            "nf_pos_create_saleorder/static/src/models/posstore.js",
            "nf_pos_create_saleorder/static/src/app/orderline/orderline.js",
            "nf_pos_create_saleorder/static/src/app/orderline/orderline.xml",
            "nf_pos_create_saleorder/static/src/app/posorder/pos_order_line.js",
            "nf_pos_create_saleorder/static/src/css/nf_saleorder_css.css",
        ],
        "point_of_sale.customer_display_assets": [],
    },
    "images": [
        "static/description/background.gif",
    ],
    "price": 25,
    "installable": True,
    "application": True,
    "auto_install": False,
    "currency": "EUR",
}
