# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": " Update User Security ",
    'author' : 'NextFlowIT',
    "website": "",
    "support": "nextflow@gmail.com",
    "category": "manufacturing",
    "summary": """ Odoo Security | Access Control | Hide Delete | Hide Archive | Hide Duplicate | User Group Security | Button Restriction | Record Security | Access Rights | Delete Restriction | Archive Restriction | Duplicate Restriction | Odoo Permissions | Odoo UI Security
        globally hide archive  remove archive to user  archive groups archive hide archive remove duplicate hide duplicate dulicate access rights update access rights access right delete access delete button hide hide delete button hide archive button duplicate archive action hide archive action duplicate action hide duplicate action delete action hide delete action remove archive action remove duplicate option remove archive option remove duplicate option 
        odoo user security  odoo access rights  odoo security management  odoo user permissions  odoo hide archive button  odoo remove archive action  odoo hide duplicate button  odoo remove duplicate action  odoo hide delete button  odoo remove delete action  odoo record action restriction  odoo user interface security  odoo admin control  odoo security customization  odoo user restriction module  odoo security settings  odoo action control odoo  odoo record management security update update security Update Security delete button odoo security
        odoo security  odoo user access control  hide delete odoo  hide duplicate odoo  hide archive odoo  odoo action restriction  odoo security settings  odoo admin control hide product sale hide hide delete button archive hide dublicate hide archive button sale order delete pos order delete purchase order delete
        odoo security odoo access control odoo hide archive button odoo hide delete button odoo hide duplicate button odoo archive restriction odoo delete restriction odoo duplicate restriction odoo user group security odoo security module odoo access rights odoo record security odoo button restriction odoo ui security odoo user permissions
    """,
    "description": """ Update Security module helps administrators control user actions in Odoo by hiding or removing the Delete, Duplicate, and Archive options. Improve system security by restricting unwanted record operations and preventing users from deleting, duplicating, or archiving records based on access rights.  """,
    # 'post_init_hook': 'post_init_hook',
    "version": "0.0.1",
    "depends": ["base", 'web', 'sale'],
    "data": [
        'security/nf_security.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'nf_update_secority/static/src/js/nf_access.js'
        ],
    },
    "images": ["static/description/background.gif", ],
    "application": True,
    "auto_install": False,
    "installable": True,
    "price": 8.00,
    "currency": "EUR",
    "license": "OPL-1",
}

