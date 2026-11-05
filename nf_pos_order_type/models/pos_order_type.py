# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import fields,models,api

class PosOrderType(models.Model):
    _name = "pos.order.type"
    _description = "Pos Order Type"
    
    name = fields.Char(string="Name")
    is_delivery = fields.Boolean(string="Delivery")
    
    @api.model
    def _load_pos_data_domain(self, data,config):
        return []
    
    def _load_pos_data_fields(self,config):
        return ['name','is_delivery']
    
    def _load_pos_data_search_read(self, records, config):
        domain = self._load_pos_data_domain(records,config)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain,fields)
        return records
        # return {
        #     'data': self.search_read(domain, fields, load=False) if domain is not False else [],
        #     'fields': fields,
        # }
    