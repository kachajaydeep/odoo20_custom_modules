# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 


from odoo import models, fields, api

class NfPosConfigInherit(models.Model):
    _inherit = 'pos.config'

    _nf_enable_dynamic_barcode_search = fields.Boolean(string="Search Dynamic Barcode ?")