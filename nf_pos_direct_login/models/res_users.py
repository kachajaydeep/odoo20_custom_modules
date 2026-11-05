# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api #type: ignore

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    pos_only_user = fields.Boolean(string='Pos Only User')
    default_pos_config_id = fields.Many2one(comodel_name='pos.config', string='Default Pos Store')
    
    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ['pos_only_user']
        return fields