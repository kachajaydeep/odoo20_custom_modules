# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api

class ResConfigPosInherit(models.TransientModel):
    _inherit = "res.config.settings"

    nf_enbale_2x_print = fields.Boolean(related="pos_config_id.nf_enbale_2x_print", readonly=False)
    nf_copy_count = fields.Integer(related="pos_config_id.nf_copy_count", readonly=False)
    
    @api.onchange('nf_copy_count')
    def _onchange_2x_print_count(self):
        if self.nf_copy_count <= 0:
            self.nf_copy_count = 1