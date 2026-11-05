# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models,fields,api

class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    nf_company_ids = fields.Many2many("res.company",string="Companies")
    nf_is_multi_company_manager = fields.Boolean(compute="_compute_is_multi_company_manager")
    
    @api.depends('nf_is_multi_company_manager')
    def _compute_is_multi_company_manager(self):
        for record in self:
            record.nf_is_multi_company_manager = self.env.user.has_group(
                'nf_product_multi_company.nf_product_multi_company_manager'
            )
    
    def action_open_nf_website_update_wizard(self):
        return {
        'type': 'ir.actions.act_window',
        'name': 'Mass Update Product Company',
        'res_model': 'nf.website.update.wizard',
        'view_mode': 'form',
        'target': 'new',  # opens as popup wizard
        'context': {
            'default_product_ids': self.ids,  # pass selected records
        },
    }
class ProductProduct(models.Model):
    _inherit = "product.product"
    
    def action_open_nf_website_update_wizard(self):
        return {
        'type': 'ir.actions.act_window',
        'name': 'Mass Update Product Company',
        'res_model': 'nf.website.update.wizard',
        'view_mode': 'form',
        'target': 'new',  # opens as popup wizard
        'context': {
            'default_product_ids': self.ids,  # pass selected records
        },
    }
        
    
