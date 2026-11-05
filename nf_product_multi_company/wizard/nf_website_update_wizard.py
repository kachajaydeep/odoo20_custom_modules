# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class NfWebsiteUpdateWizard(models.TransientModel):
    _name = 'nf.website.update.wizard'
    _description = 'Mass Update Websites for Products'

    nf_company_ids = fields.Many2many("res.company",string="Companies")

    def action_update_websites(self):
        active_ids = self.env.context.get('active_ids')
        active_model = self.env.context.get('active_model')

        if active_ids:
            products = self.env['product.template'].browse(active_ids)
            product_variants = self.env['product.product'].browse(active_ids)
            if active_model == 'product.template':
                products.write({'nf_company_ids': [(6, 0, self.nf_company_ids.ids)]})
            else:
                variants = self.env['product.product'].browse(active_ids)
                products = variants.mapped('product_tmpl_id')

            products.write({
                'nf_company_ids': [(6, 0, self.nf_company_ids.ids)]
            })