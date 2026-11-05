# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api

class NfAssignBrandWizard(models.TransientModel):
    _name = 'nf.assign.brand.wizard'
    _description = 'Assign Brand Wizard'

    nf_product_brand_id = fields.Many2one('product.brands', string="Brand", required=True)

    def action_assign_brand(self):
        active_ids = self.env.context.get('active_ids', [])
        active_model = self.env.context.get('active_model')

        if active_model == 'product.template' and active_ids:
            records = self.env['product.template'].browse(active_ids)
            records.write({'nf_product_brand_id': self.nf_product_brand_id.id})
        elif active_model == 'product.product' and active_ids:
            records = self.env['product.product'].browse(active_ids)
            templates = records.mapped('product_tmpl_id')
            templates.write({'nf_product_brand_id': self.nf_product_brand_id.id})
