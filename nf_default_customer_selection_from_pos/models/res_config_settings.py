# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    nf_is_default_selection_customer = fields.Boolean(related='pos_config_id.nf_is_default_selection_customer',readonly=False)
    nf_default_customer_id = fields.Many2one(related='pos_config_id.nf_default_customer_id',readonly=False)