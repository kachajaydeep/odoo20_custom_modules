# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class PosConfigInherited(models.Model):
    _inherit = 'pos.config'
    
    nf_enable_direct_login = fields.Boolean('Enable Direct Login', default=False)