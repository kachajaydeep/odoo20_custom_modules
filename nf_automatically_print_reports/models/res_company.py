# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    nf_automatically_print_pdf_report = fields.Boolean(string="Automatically Print Pdf Report")
    
    
