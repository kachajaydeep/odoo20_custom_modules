# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields, api #type: ignore

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    nf_enable_receipt_barcode = fields.Boolean(related='pos_config_id.nf_enable_receipt_barcode', readonly=False)
    nf_barcode_prefix = fields.Char(related='pos_config_id.nf_barcode_prefix', readonly=False, required=True)