# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, _, http

class Product(models.Model):
    _inherit = "product.template"

    nf_box_item_count = fields.Integer(string="Box Item (Qty)")