# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import api, models

class PosSession(models.Model):
    _inherit = 'pos.session'
    
    @api.model
    def get_bag_templates_by_category(self, config_id, category_id):
        if not category_id:
            return []

        templates = self.env['product.template'].search_read(
            domain=[
                ('pos_categ_ids', 'in', [category_id]),
                ('available_in_pos', '=', True),
                ('sale_ok', '=', True),
                ('active', '=', True),
            ],
            fields=[
                'id', 'name', 'display_name', 'list_price',
                'pos_categ_ids', 'taxes_id',
                'product_variant_ids',
            ],
        )

        for tmpl in templates:
            variants = self.env['product.product'].search_read(
                domain=[
                    ('product_tmpl_id', '=', tmpl['id']),
                    ('active', '=', True),
                ],
                fields=[
                    'id', 'display_name', 'lst_price',
                    'product_template_attribute_value_ids',
                ],
            )
            tmpl['variants'] = variants
        print("\n\n\n\n templates ?????",templates)
        return templates
