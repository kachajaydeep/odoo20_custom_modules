# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api

class PosThemeSettings(models.Model):
    _name = 'nf.pos.theme.settings'
    _inherit = ['pos.load.mixin']
    _description = 'POS Theme Settings'

    name = fields.Char(string='Name', required=True)
    logo = fields.Binary(string='Header Logo', attachment=True)
    product_view_selection = fields.Selection([
        ('grid', 'Grid View'),
        ('list', 'List View'),
    ], string='Default Product View', default='grid', required=True)

    # def _load_pos_data(self, data):
    #     domain = []
    #     fields = []
    #     themes = self.search_read(domain, load=False)

    #     # themes.read(fields, load=False)
    #     return {
    #         'data': themes,
    #         'fields': fields,
    #     }
    @api.model
    def _load_pos_data_domain(self,record,config):
        return []
    
    @api.model
    def _load_pos_data_fields(self,config):
        return []
    
    def _load_pos_data_search_read(self,record,config):
        domain = self._load_pos_data_domain(record,config)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain,fields)
        return records
    
class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config):
        models = super()._load_pos_data_models(config)
        models += ['nf.pos.theme.settings']
        return models
