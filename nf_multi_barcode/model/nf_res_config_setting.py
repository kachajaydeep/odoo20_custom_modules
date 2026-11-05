# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields

class NfResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    nf_multi_barcode_unique = fields.Boolean(related='company_id.nf_multi_barcode_unique', string="Is Multi Barcode Unique", readonly=False)