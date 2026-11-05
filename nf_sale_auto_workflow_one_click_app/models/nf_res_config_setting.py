# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo  import models, fields, api

class NfResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    nf_enable_one_click_sale = fields.Boolean(related="company_id.nf_enable_one_click_sale", readonly=False, string="Enable One Click Sale")
    nf_validate_delivery = fields.Boolean(related="company_id.nf_validate_delivery", readonly=False, string="Validate Delivery")
    nf_create_invoice = fields.Boolean(related="company_id.nf_create_invoice", readonly=False, string="Create Invoice")
    nf_pay_invoice = fields.Boolean(related="company_id.nf_pay_invoice", readonly=False, string="Pay Invoice")
    
    @api.onchange('nf_enable_one_click_sale','nf_create_invoice')
    def _onchange_(self):
        if not self.nf_create_invoice:
            self.nf_pay_invoice = False
            
        if not self.nf_enable_one_click_sale:
            self.nf_validate_delivery = False
            self.nf_create_invoice = False
            self.nf_pay_invoice = False
        