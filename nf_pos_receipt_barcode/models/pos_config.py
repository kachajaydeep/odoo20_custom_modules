# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields #type: ignore

class PosConfig(models.Model):
    _inherit = "pos.config"

    nf_enable_receipt_barcode = fields.Boolean(string="Receipt Barcode")
    nf_barcode_prefix = fields.Char(string='Barcode Prefix')
    
    def write(self, vals):
        result = super().write(vals)
        if 'nf_barcode_prefix' in vals or 'nf_enable_receipt_barcode' in vals:
            for config in self:
                barcode_rule = self.env.ref(
                    'nf_pos_receipt_barcode.barcode_rule_receipt',
                    raise_if_not_found=False
                )
                if barcode_rule:
                    prefix = config.nf_barcode_prefix
                    if config.nf_enable_receipt_barcode and prefix and isinstance(prefix, str):
                        barcode_rule.write({
                            'pattern': prefix,
                        })
                    elif not config.nf_enable_receipt_barcode:
                        barcode_rule.write({
                            'pattern': 'NF',
                        })
        return result