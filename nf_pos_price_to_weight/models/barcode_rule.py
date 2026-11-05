# -*- coding: utf-8 -*-
# Part of NextFlowIT.

from odoo import fields, models

class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'

    type = fields.Selection(selection_add=[
        ('price_to_weight', 'Priced to weight Product')
        ],ondelete={'price_to_weight': 'cascade'}
    )