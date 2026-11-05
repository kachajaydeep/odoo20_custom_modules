# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _load_pos_data_fields(self,config):
        model_fields = super()._load_pos_data_fields(config)
        model_fields.extend(['qty_available','location_id','type'])
        return model_fields
    
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    @api.model
    def _load_pos_data_fields(self,config):
        model_fields = super()._load_pos_data_fields(config)
        model_fields.extend(['product_variant_id'])
        return model_fields
    
class StockPicking(models.Model):
    _inherit = "stock.picking.type"

    @api.model
    def _load_pos_data_fields(self,config):
        model_fields = super()._load_pos_data_fields(config)
        model_fields.extend(['default_location_src_id'])
        return model_fields
    