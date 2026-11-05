# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, api

class PosSession(models.Model):
    _inherit = 'pos.session'
    
    @api.model
    def _load_pos_data_models(self, config_id):
        models = super()._load_pos_data_models(config_id)
        if 'stock.lot' not in models:
            models.append("stock.lot")
        return models
    
class StockLot(models.Model):
    _name = "stock.lot"
    _inherit = ["stock.lot", "pos.load.mixin"]
    
    @api.model
    def _load_pos_data_fields(self, config_id):
        return ['id', 'name', 'product_id', 'product_qty', 'quant_ids', 'uom_id']
    
    @api.model
    def get_pos_lots(self, product_id):
        lots = self.search([("product_id", "=", product_id)])

        return [
            {
                "id": lot.id,
                "name": lot.name,
                "product_id": lot.product_id.id,
                "product_qty": lot.product_qty,
            }
            for lot in lots
        ]