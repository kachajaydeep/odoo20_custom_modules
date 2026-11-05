# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields, api

class Partner(models.Model):
    _inherit='res.partner'

    @api.model_create_multi
    def create(self, vals):
        partners = super().create(vals)
        pos_session_sudo = self.env["pos.session"].sudo().search([('state','in',['opening_control', 'opened'])])
        for session in pos_session_sudo:
            session.config_id._notify("nfPartnerCreated", partners.ids)
        return partners