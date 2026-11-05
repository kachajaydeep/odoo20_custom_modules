# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api, _


class Respartner(models.Model):
    _inherit = "res.partner"

    nf_city_id = fields.Many2one('nf.cities', string="City")

    @api.onchange('nf_city_id')
    def _onchange_nf_city_id(self):
        self.city = self.nf_city_id.name