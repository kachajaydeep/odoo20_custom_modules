# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, api

class NfMultiBarcodeInherit(models.Model):
    _name = 'nf.multi.barcode'
    _inherit = ['nf.multi.barcode', 'pos.load.mixin']
    
    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ['name','nf_product_id','nf_product_template_id']
        return fields
    
    @api.model
    def _load_pos_data_domain(self, data, config):
        product_ids = [
            product['id']
            for product in data.get('product.product', [])
        ]

        template_ids = [
            template['id']
            for template in data.get('product.template', [])
        ]

        return [
            '|',
            ('nf_product_id', 'in', product_ids),
            ('nf_product_template_id', 'in', template_ids),
        ]