# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    nf_automatically_print_pdf_report = fields.Boolean(string="Automatically Print Pdf Report",related="company_id.nf_automatically_print_pdf_report",readonly=False)