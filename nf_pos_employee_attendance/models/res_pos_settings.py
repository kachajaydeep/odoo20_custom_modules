# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields

class ResConfigPosInherit(models.TransientModel):
    _inherit = "res.config.settings"

    nf_enbale_check_in_out = fields.Boolean(related="pos_config_id.nf_enbale_check_in_out", readonly=False)