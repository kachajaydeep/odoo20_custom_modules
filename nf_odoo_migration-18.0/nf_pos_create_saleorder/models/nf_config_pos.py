# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api

class POSConfigInherit(models.Model):
    _inherit = 'pos.config'

    nf_enable_create_saleorder = fields.Boolean(string='Want to Create Sale Order from POS?')

class ProductInherit(models.Model):
    _inherit = 'product.product'

    nf_demo_product_for_sale_section = fields.Boolean()

    @api.model
    def _load_pos_data_fields(self, config_id):
        res = super()._load_pos_data_fields(config_id)
        res += ['nf_demo_product_for_sale_section']
        return res

    def _load_pos_data(self, data):
        res = super()._load_pos_data(data)
        res['data'] += self.env.ref('nf_pos_create_saleorder.nf_demo_product_for_section').read(self._load_pos_data_fields(data['pos.config']['data'][0]['id']),load=False)
        return res

class PosOrderlineinherit(models.Model):
    _inherit = 'pos.order.line'

    nf_section = fields.Char(string='Section')

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.model
    def NfPosCreateSaleOrder(self, vals):
        print('\n\n\n -----vals----->',vals)
        QuotationList = []
        saleOrderlist = []
        if vals:
            for val in vals:
                if val:
                    quotationdic = {}
                    saleOrderdic = {}
                    saleOrder = self.create({'partner_id': val.get('partner_id')})
                    if saleOrder:
                        if val.get('sale_order_lines'):
                            for line in val.get('sale_order_lines'):
                                line.update({'order_id': saleOrder.id})
                                print('line-->',line)
                                self.env['sale.order.line'].create(line)

                        if val.get('is_confirm'):
                            saleOrder.action_confirm()
                            quotationdic.update({'order_id': saleOrder.id, 'order_name': saleOrder.name,'sale_order_state': 'sale_order'})
                            saleOrderlist.append(quotationdic)
                        else:
                            saleOrderdic.update({'order_id': saleOrder.id, 'order_name': saleOrder.name})
                            QuotationList.append(saleOrderdic)

                            
        return {'QuotationList':QuotationList, 'saleOrderlist': saleOrderlist}
    
class PosSession(models.Model):
    _inherit="pos.session"

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('nf_demo_product_for_sale_section')
        return result