# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _load_pos_data_fields(self, config):
        result=super()._load_pos_data_fields(config)
        result+=["seller_ids"]
        return result

class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    @api.model
    def _load_pos_data_domain(self, data,config_id):
        return []
    
    @api.model
    def _load_pos_data_fields(self,config_id):
        return []
    
    def _load_pos_data_search_read(self, records, config_id):
        domain = self._load_pos_data_domain(records,config_id)
        fields = self._load_pos_data_fields(config_id)
        records = self.search_read(domain,fields,load=False)
        return records
        

class ProductTemplate(models.Model):
    _inherit = 'product.template'
      
class PosSession(models.Model):
    _inherit = "pos.session"

    @api.model
    def _load_pos_data_models(self, config):
        record = super()._load_pos_data_models(config)
        record += ["product.supplierinfo"]
        return record