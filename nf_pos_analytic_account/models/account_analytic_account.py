# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import api, fields, models, _

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    
    @api.model
    def _load_pos_data_domain(self,data,config):
        return []
    
    @api.model
    def _load_pos_data_fields(self,config):
        return []
    
    def _load_pos_data_search_read(self,record,config):
        domain = self._load_pos_data_domain(record,config)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain,fields)
        return records