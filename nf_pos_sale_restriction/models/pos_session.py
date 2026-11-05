# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api, _

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_data_process(self, loaded_data):
        super()._pos_data_process(loaded_data)

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(["qty_available", 'location_id', "type"])
        return result

    def _loader_params_stock_picking_type(self):
        result = super()._loader_params_stock_picking_type  ()
        result['search_params']['fields'].append('default_location_src_id')
        return result

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        if 'stock.location' not in result:
            result.append('stock.location')
        if 'stock.quant' not in result:
            result.append('stock.quant')
        return result

    def _loader_params_stock_location(self):
        return {'search_params': {'domain': [("location_id", "=", self.config_id.picking_type_id.default_location_src_id.id)], 'fields': [], 'load': False}}

    def _get_pos_ui_stock_location(self, params):
        return self.env['stock.location'].search_read(**params['search_params'])
        
    def _loader_params_stock_quant(self):
        return {'search_params': {'domain': [('location_id', '=', self.config_id.picking_type_id.default_location_src_id.id)], 'fields': [], 'load': False}}

    def _get_pos_ui_stock_quant(self, params):
        return self.env['stock.quant'].search_read(**params['search_params'])
