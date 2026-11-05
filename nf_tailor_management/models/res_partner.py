# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    measurement_ids = fields.One2many('nf.measurement', 'partner_id', string="measurement")