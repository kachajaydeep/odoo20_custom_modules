# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class PosConfig(models.Model):
    _inherit = "pos.config"

    nf_check_stock = fields.Boolean(string="Check Stock Availibility")
    nf_allow_to_sale = fields.Boolean(string="Allow Negative Selling ")

class ResPosSetting(models.TransientModel):
    _inherit = "res.config.settings"

    nf_check_stock = fields.Boolean(related="pos_config_id.nf_check_stock", readonly=False)
    nf_allow_to_sale = fields.Boolean(related="pos_config_id.nf_allow_to_sale", readonly=False)


class StockQuant(models.Model):
    _inherit="stock.quant"

    def nf_check_availibility(self, product_id):
        _logger.info("NF STOCK: product_id = %s", product_id)

        if not product_id:
            return {'qty': 0.0}

        stocks = self.sudo().search([
            ('product_id', '=', int(product_id)),
            ('location_id.usage', '=', 'internal'),
        ])

        qty = sum(stocks.mapped('available_quantity'))
        _logger.info("NF STOCK: qty = %s", qty)

        return {'qty': qty}