# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': "Product Variant Display From Point of Sale",
    'summary': """""",
    'post_init_hook': 'post_init_hook',
    'description': """""",
    'author': 'NextFlowIT',
    'license': "OPL-1",
    'company': 'NextFlow Technology',
    'maintainer': 'NextFlow Technology',
    'website': 'nextflow.in',
    'version': '20.0.1',
    'depends': ['point_of_sale'],
    'data': [
        'views/res_config_settings.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_pos_product_variant_display/static/src/overrides/product_configurator_popup/product_configurator_popup.js',
            'nf_pos_product_variant_display/static/src/overrides/product_configurator_popup/product_configurator_popup.xml',
            'nf_pos_product_variant_display/static/src/overrides/product_configurator_popup/product_configurator_popup.scss',
            # 'nf_pos_product_variant_display/static/src/overrides/ProductInfoBanner/ProductInfoBanner.xml',
            # 'nf_pos_product_variant_display/static/src/overrides/ProductInfoBanner/ProductInfoBanner.js',
            # 'nf_pos_product_variant_display/static/src/overrides/ProductInfoBanner/ProductInfoBanner.scss',
            # 'nf_pos_product_variant_display/static/src/overrides/product_card/product_card.js',
            # 'nf_pos_product_variant_display/static/src/overrides/product_card/product_card.xml',
            # 'nf_pos_product_variant_display/static/src/overrides/product_card/product_card.scss',
        ],
    },
    "images": ["static/description/background.gif"],
    'application': False,
    'installable': True,
    'auto_install': False,
    "price": 79.99,
    "currency": "USD"
}