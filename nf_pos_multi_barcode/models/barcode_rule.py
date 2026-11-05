# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields # type: ignore

class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'

    type = fields.Selection(selection_add=[
        ('multi_barcode', 'Product Multi Barcode'),
    ], ondelete={
        'multi_barcode': 'set default',
    })