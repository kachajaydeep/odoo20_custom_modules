# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields #type: ignore

class PosConfigInherited(models.Model):
    _inherit = 'pos.config'
    
    allow_secondary_uom = fields.Boolean(string='Allow Secondary UOM')