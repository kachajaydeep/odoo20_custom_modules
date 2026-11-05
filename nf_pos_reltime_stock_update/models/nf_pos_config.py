# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api

class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    nf_pos_enable_realtime_stock_update = fields.Boolean(string="Enable Realtime Stock Update")

    def send_notification(self, vals):
        session_ids = self.env['pos.session'].search([('state', 'in', ['opening_control', 'opened']), ('config_id','!=', vals.get('config_id'))])
        Details = self.env['stock.quant'].search_read([('product_id', '=', vals.get('product_id')),('location_id', '=',vals.get('location_id')), ('location_id.usage','=','internal')],  ['product_id', 'location_id', 'quantity', 'product_tmpl_id', 'available_quantity'], load=False)
        
        if Details:
            final_dic = Details[0]
            if vals.get('minus_quantity'):
                final_dic['stock_adjustments'] = False
                final_dic['minus_quantity'] = vals.get('minus_quantity') 
            else:
                final_dic['stock_adjustments'] = True
            if session_ids:
                for Session in session_ids:
                    final_dic['config_id'] = Session.config_id.id
                    Session.config_id._notify("nf_update_stock", {'config_id': Session.config_id.id, 'StockUpdate': final_dic })
                    
        else:
            Details ={'product_id': vals.get('product_id'), 'location_id': vals.get('location_id'), 'quantity': 0.0,  'available_quantity': 0.0, 'stock_adjustments': False, 'minus_quantity': vals.get('minus_quantity'), 'config_id':  vals.get('config_id')}
            # print('\n\n\n ----->',Details)
            if session_ids:
                for Session in session_ids:
                    Details['config_id'] = Session.config_id.id
                    Session.config_id._notify("nf_update_stock", {'config_id': Session.config_id.id, 'StockUpdate': Details })