# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields, api, _
from odoo.fields import Domain
from odoo.exceptions import UserError, ValidationError


class NfProductProduct(models.Model):
    _inherit = 'product.product'

    nf_multi_barcode_unique = fields.Boolean(compute="_compute_nf_multi_barcode_unique")
    barcode_ids = fields.One2many('nf.multi.barcode' ,'nf_product_id')
    
    def _compute_nf_multi_barcode_unique(self):
        for rec in self:
            rec.nf_multi_barcode_unique = self.env.company.nf_multi_barcode_unique    
    
    @api.constrains('barcode_ids')
    def _constrains_barcode_ids_unique(self):
        for record in self:
            for barcode_id in record.barcode_ids:
                existing = self.env['nf.multi.barcode'].search([('name','=',barcode_id.name),('id','!=',barcode_id.id)])
                if existing:
                    raise ValidationError(_(f"Barcode already exists. {barcode_id.name}"))
    
    
    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        if not name:
            return super().name_search(name, domain, operator, limit)

        positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
        is_positive = operator not in Domain.NEGATIVE_OPERATORS
        products = self.browse()
        domain = Domain(domain or Domain.TRUE)

        if operator in positive_operators:
            products = (
                self.search_fetch(domain & Domain('default_code', '=', name), ['display_name'], limit=limit)
                or self.search_fetch(domain & Domain('barcode', '=', name), ['display_name'], limit=limit)
                or self.search_fetch(domain & Domain('barcode_ids.name', '=', name), ['display_name'], limit=limit)
            )

        if not products and is_positive:
            products = self.search_fetch(domain & Domain('default_code', operator, name), ['display_name'], limit=limit)
            limit_rest = limit and limit - len(products)

            if limit_rest is None or limit_rest > 0:
                products |= self.search_fetch(
                    domain & Domain('barcode_ids.name', operator, name),
                    ['display_name'],
                    limit=limit_rest
                )

                limit_rest = limit and limit - len(products)

                if limit_rest is None or limit_rest > 0:
                    products |= self.search_fetch(
                        domain & Domain('name', operator, name),
                        ['display_name'],
                        limit=limit_rest
                    )

        if not products:
            return super().name_search(name, domain, operator, limit)

        return [(product.id, product.display_name) for product in products.sudo()]
