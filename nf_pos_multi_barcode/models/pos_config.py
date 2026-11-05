# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class PosConfigInherit(models.Model):
    _inherit = 'pos.config'
    
    nf_enable_pos_multi_barcode = fields.Boolean('Enable Multi Barcode for Pos')