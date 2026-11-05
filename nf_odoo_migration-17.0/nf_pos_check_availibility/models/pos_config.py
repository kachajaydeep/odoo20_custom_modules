# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = "pos.config"

    nf_check_stock = fields.Boolean(string="Check Stock Availibility")
    nf_allow_to_sale = fields.Boolean(string="Allow Negative Selling ")

class ResPosSetting(models.TransientModel):
    _inherit = "res.config.settings"

    nf_check_stock = fields.Boolean(related="pos_config_id.nf_check_stock", readonly=False)
    nf_allow_to_sale = fields.Boolean(related="pos_config_id.nf_allow_to_sale", readonly=False)


class StockQuont(models.Model):
    _inherit="stock.quant"

    def nf_check_availibility(self,  product_id):
        stocks = self.search([('product_id', '=', product_id), ('location_id.usage', 'in', ('internal',))])

        return stocks.available_quantity if stocks else 0