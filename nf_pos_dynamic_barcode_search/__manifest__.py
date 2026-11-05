# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Point Of Sale Dynamic Barcode Search',
    'summary': """ point of sale dynamic barcode search dynamic search barcode search search by barcode dynamic search pos dynamic barcode search dynamic search pos search Barcode Nomenclature pos barcode nomenclature  """,
    'author': 'NextFlowIT',
    "license": "OPL-1",
    'description': """ Easyly search dynamic barcode in pos  """,
    'category': "Point of sale",
    'website': '',
    'depends': ['point_of_sale'],
    'version': '15.0.1',
    'data': [
        'views/nf_pos_configuration.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'nf_pos_dynamic_barcode_search/static/src/scss/nf_pos_scss.scss',
            'nf_pos_dynamic_barcode_search/static/src/js/nf_pos_search_barcode.js'
        ],
        'web.assets_qweb': [
            'nf_pos_dynamic_barcode_search/static/src/xml/nf_pos_search_barcode.xml'
        ]
    },
    "images": ["static/description/background.png", ],
    "price": 35.42,
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR"
}
