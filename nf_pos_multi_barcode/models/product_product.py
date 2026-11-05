# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, api

class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    
    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ['barcode_ids']
        return fields
    
    
class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    
    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ['barcode_ids']
        return fields