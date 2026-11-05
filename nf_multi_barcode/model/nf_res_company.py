# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models


class NfResCompany(models.Model):
    _inherit = 'res.company'

    nf_multi_barcode_unique = fields.Boolean(string="Is Multi Barcode Unique")