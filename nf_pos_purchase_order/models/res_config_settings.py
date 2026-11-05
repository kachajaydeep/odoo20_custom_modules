# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    create_po = fields.Boolean(
        related="pos_config_id.create_po",
        string="Create Purchase Order",
        readonly=False,
    )
    po_status = fields.Selection(
        related="pos_config_id.po_status", string="PO Status", readonly=False
    )
    validate_po_receipt = fields.Boolean(
        related="pos_config_id.validate_po_receipt",
        string="Validate Receipt",
        readonly=False,
    )
    create_bill = fields.Boolean(
        related="pos_config_id.create_bill", string="Create Bill", readonly=False
    )

    @api.onchange("po_status")
    def _onchange_po_status(self):
        if self.po_status != "purchase":
            self.validate_po_receipt = False
            self.create_bill = False

    @api.onchange("create_bill")
    def _onchange_create_bill(self):
        if self.create_bill:
            self.validate_po_receipt = True