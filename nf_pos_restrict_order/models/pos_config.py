# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.


from odoo import models, fields, api


class PosConfigInherit(models.Model):
    _inherit = "pos.config"

    nf_pos_restrict_out_of_stock = fields.Boolean(
        string="Restrict out of stock order creatoin ?"
    )
