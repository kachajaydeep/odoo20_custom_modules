# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api, _

class ResConfigPosInherit(models.TransientModel):
    _inherit = "res.config.settings"

    nf_pos_enable_realtime_stock_update = fields.Boolean(related="pos_config_id.nf_pos_enable_realtime_stock_update", readonly=False)