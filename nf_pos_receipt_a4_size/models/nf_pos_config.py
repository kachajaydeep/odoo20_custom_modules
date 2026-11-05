# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields


class NftPosConfigInherit(models.Model):
    _inherit = "pos.config"

    _nf_enable_a4_size_receipt = fields.Boolean(string="Enable A4 size Receipt Print")


class NftCompanyInherit(models.Model):
    _inherit = "res.company"

    _nf_show_arabic_labels = fields.Boolean()


class pos_order(models.Model):
    _inherit = "pos.order"

    qr_code_img = fields.Char(string="Qr Code")

    def _order_fields(self, ui_order):
        res = super(pos_order, self)._order_fields(ui_order)

        if ui_order.get("qr_img"):
            res.update(
                {
                    "qr_code_img": (
                        ui_order.get("qr_img") if ui_order.get("qr_img") else False
                    ),
                }
            )
        return res
