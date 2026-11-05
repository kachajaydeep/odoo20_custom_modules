# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api    #type: ignore

class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    
    is_default_uom = fields.Boolean(string='Add Default UOM')
    default_uom_id = fields.Many2one('uom.uom', string='Default UOM', help="Default UOM which will be used for product in Pos Store.", domain="[('id', '!=', uom_id)]")
    uom_ids = fields.Many2many('uom.uom', string='Packagings', help="Additional packagings for this product which can be used in Pos.", domain="[('id', '!=', uom_id)]")
    
    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ["uom_ids", "default_uom_id", "is_default_uom"]
        return fields
    
    @api.model
    def get_price_for_uom(self, product_tmpl_id, uom_id):
        product = self.browse(product_tmpl_id)
        uom = self.env['uom.uom'].browse(uom_id)
        
        return product.uom_id._compute_price(product.list_price, uom)
    
    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        for product in products:
            if product.uom_id and product.uom_id not in product.uom_ids:
                product.uom_ids = [(4, product.uom_id.id)]
        return products

    def write(self, vals):
        res = super().write(vals)
        for product in self:
            if product.uom_id and product.uom_id not in product.uom_ids:
                product.uom_ids = [(4, product.uom_id.id)]
        return res