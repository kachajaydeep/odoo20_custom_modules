# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api

class StockUpdate(models.Model):
    _inherit = 'stock.quant'
            
    def write(self, vals):
        res = super(StockUpdate, self).write(vals)
        PosSessions = self.env['pos.session'].search([('state', 'in', ['opening_control', 'opened']), ('config_id','!=', vals.get('config_id'))])
        if (vals and not vals.get('reserved_quantity') and self.location_id.usage == 'internal'):
            for quant in self:
                if PosSessions:
                    for Session in PosSessions:
                        Details = self.search_read([('product_id', '=', quant.product_id.id),('location_id', '=', Session.config_id.picking_type_id.default_location_src_id.id), ('location_id.usage','=','internal')],  ['product_id', 'location_id', 'quantity', 'product_tmpl_id', 'available_quantity'], load=False)
                        if Details:
                            final_dic = Details[0]
                            if vals.get('reserved_quantity'):
                                final_dic['stock_adjustments'] = False
                                final_dic['minus_quantity'] = vals.get('reserved_quantity')
                                
                            else:
                                final_dic['stock_adjustments'] = True
                                final_dic['config_id'] = Session.config_id.id
                                Session.config_id._notify("nf_update_stock", {'config_id': Session.config_id.id, 'StockUpdate': final_dic })
                            
        return res
    
class Product(models.Model):
    _inherit='product.product'

    bool_for_realtime_update = fields.Boolean('bool_for_realtime_update')

    @api.model
    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result.extend(["bool_for_realtime_update"])
        return result