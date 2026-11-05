# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api
import base64

class PosConfig(models.Model):
    _inherit = 'pos.config'

    nf_direct_print_invoice = fields.Boolean(string="Auto Print Invoice!")

    @api.model
    def getInvoicePrint(self, id): 
        inv = self.env['ir.actions.report']._render_qweb_pdf('account.account_invoices', res_ids=[id])[0]
        return base64.b64encode(inv)