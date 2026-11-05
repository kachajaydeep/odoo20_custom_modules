# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.


{
    "name" : "Section Remove Workflow",
    "summary" : """
        add a section delete odoo sale section delete section remove order line sale order line delete section section sale order line remove section purchase order line remove section purchase order line delete section invoice line remove section bill line remove section orderline delete orderline remove section delete odoo section delete odoo delete section with lines odoo sales order section delete odoo purchase order section delete odoo invoice section delete odoo bill section delete odoo section management odoo line section workflow odoo document section delete odoo quotation section delete odoo rfq section delete odoo accounting section management odoo invoice line section odoo purchase line section odoo sales line section odoo section cleanup odoo productivity module odoo user friendly section delete odoo document organization odoo section delete wizard odoo section line removal odoo erp enhancement odoo business process automation odoo sales purchase accounting module odoo section workflow module purchase section order line section
    """,
    # 'post_init_hook': 'post_init_hook',
    
    "description" : """
        Efficiently delete sections in Sales Orders, Purchase Orders, Customer Invoices, and Vendor Bills. Choose to remove only the section or delete the section with all related lines using a simple wizard directly from the section menu in Odoo.
    """,
    "data" : [
            'views/nf_account_move_view.xml',
            'views/nf_purchase_order_view.xml',
            'views/nf_sale_order_view.xml',
        ],
    
    "assets" : {
        'web.assets_backend': [
            "nf_section_delete_workflow/static/src/js/nf_patch_section.js",
            "nf_section_delete_workflow/static/src/js/nf_add_section_delete_dialog.js",
            "nf_section_delete_workflow/static/src/xml/nf_add_section_delete_dialog.xml",
        ]
    },
    "support": "nextflow@gmail.com",
    "author": 'NextFlowIT',
    "company": 'NextFlow Technology',
    "maintainer": 'NextFlow Technology',
    "website": 'https://www.nextflow.in',
    "version": "0.0.1",
    "depends" : ['base', 'purchase', 'account', 'sale_management', 'product'],
    "license": 'OPL-1',
    "images": ["static/description/background.gif"],
    "installable" : True,
    "application": True,
    "auto_install": False,
    "price": 12,
    "currency": "USD"
    
}
