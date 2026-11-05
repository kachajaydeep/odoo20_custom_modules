# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import api, fields, models

class PosConfig(models.Model):
    _inherit = "pos.config"

    create_po = fields.Boolean(string="Create Purchase Order", default=False)
    po_status = fields.Selection([
            ("draft", "RFQ"),
            ("sent", "RFQ Sent"),
            ("purchase", "Purchase Order"),
        ],
        string="PO Status",
        default="draft",
    )
    validate_po_receipt = fields.Boolean("Validate Receipt", default=False)
    create_bill = fields.Boolean("Create Bill", default=False)
    
    @api.onchange('po_status')
    def _onchange_po_status(self):
        if self.po_status != 'purchase':
            self.validate_po_receipt = False
            self.create_bill = False

    @api.onchange('create_bill')
    def _onchange_create_bill(self):
        if self.create_bill:
            self.validate_po_receipt = True