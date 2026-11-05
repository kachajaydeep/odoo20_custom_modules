# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields,api

class NfReceiptTemplate(models.Model):
    _name = 'nf.receipt.template'
    _description = 'Receipt Template'
    _rec_name = 'nf_receipt_name'

    nf_receipt_name = fields.Char(string="Name")
    nf_receipt_xml = fields.Text(string="Receipt XML")

    @api.model
    def _load_pos_data_domain(self, data):
        """ Return the domain used to filter records """
        return []

    @api.model
    def _load_pos_data_fields(self, config):
        """ Return the list of fields to be loaded """
        return ['nf_receipt_name', 'nf_receipt_xml']
