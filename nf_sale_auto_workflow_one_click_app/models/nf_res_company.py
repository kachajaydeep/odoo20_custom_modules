# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo  import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    nf_enable_one_click_sale = fields.Boolean(string="Enable One Click Sale")
    nf_validate_delivery = fields.Boolean(string="Validate Delivery")
    nf_create_invoice = fields.Boolean(string="Create Invoice")
    nf_pay_invoice = fields.Boolean(string="Pay Invoice")