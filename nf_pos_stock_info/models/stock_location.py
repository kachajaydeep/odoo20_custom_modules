# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api, _ 


class StockLocation(models.Model):
    _inherit = "stock.location"

    def _load_pos_data_domain(self,data,config):
        config_id = config.id
        location_ids = [config.picking_type_id.default_location_src_id.id]

        if config.picking_type_id.default_location_src_id.child_ids:
            location_ids.extend(config.picking_type_id.default_location_src_id.child_ids.ids)
        return [('id','in',location_ids)]

    def _load_pos_data_fields(self,config):
        return []
    
    def _load_pos_data_search_read(self,data,config):

        domain = self._load_pos_data_domain(data,config)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain,fields,load=False)
        return records
    