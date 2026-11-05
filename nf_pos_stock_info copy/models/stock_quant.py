# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api, _ 

 
class StockQuant(models.Model):
    _inherit = ['stock.quant', 'pos.load.mixin']

    @api.model
    def _load_pos_data_domain(self,config):
        config_id = config['pos.config']['id']
        config = self.env['pos.config'].browse(config_id)
        location_ids = [config.picking_type_id.default_location_src_id.id]
        if config.picking_type_id.default_location_src_id.child_ids:
            location_ids.extend(config.picking_type_id.default_location_src_id.child_ids.ids)
        return [('location_id', 'in', location_ids)]
    
    @api.model
    def get_product_quantity_for_pos(self, config, product_id):
        domain = self._load_pos_data_domain(config)
        domain.append(('product_id', '=', product_id))
        quants = self.search(domain)
        return sum(quants.mapped('quantity'))

    def _load_pos_data_fields(self,config):
        return ['location_id', 'display_name', 'uom_id', 'product_id', 'quantity', 'available_quantity']
        
    def _load_pos_data_search_read(self,data,config):
        domain =self._load_pos_data_domain(config)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain,fields, load=False)
        
        # return record
        merged_records = {}
        for rec in records:
            # Key should be (product_id (int), location_id (int))
            # Odoo search_read with load=False returns IDs for M2O fields
            prod_id = rec.get('product_id')
            loc_id = rec.get('location_id')
            key = (prod_id, loc_id)
            
            if key not in merged_records:
                merged_records[key] = rec.copy()
            else:
                merged_records[key]['quantity'] += rec.get('quantity', 0.0)
                merged_records[key]['available_quantity'] += rec.get('available_quantity', 0.0)
                
        return list(merged_records.values())
