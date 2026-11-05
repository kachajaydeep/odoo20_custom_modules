# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 


from odoo import models, fields, api

class NfAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    nf_brand_id = fields.Many2one(related='product_id.nf_product_brand_id', string="Brand")


class NfAccountMove(models.Model):
    _inherit = 'account.move'
       
    nf_invoice_line_brand_enable = fields.Boolean(compute="_compute_invoice_line_brand_enable")
    nf_brand_invoice_report_enable = fields.Boolean(compute="_compute_brand_invoice_report_enable")
    
            
    @api.depends_context('company')
    def _compute_invoice_line_brand_enable(self):
        for rec in self:
            rec.nf_invoice_line_brand_enable = rec.env.company.nf_product_brand_on_view_enable
            
    @api.depends_context('company')
    def _compute_brand_invoice_report_enable(self):
        for rec in self:
            rec.nf_brand_invoice_report_enable = rec.env.company.nf_product_brand_report_enable