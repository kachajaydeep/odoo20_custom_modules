# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

import qrcode
import base64

from hashlib import sha1
from io import BytesIO
from odoo import fields, models, api, _
from odoo.tools import BinaryBytes


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    qr_code = fields.Binary(string='QR Code', compute="_compute_qr_code",
                            help="Use POS Login with QR Code", store=True)

    @api.depends('pin')
    def _compute_qr_code(self):
        for employee in self:
            if employee.pin:
                qr_code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3,
                                        border=4, )
                qr_code.add_data(sha1(employee.pin.encode()).hexdigest())
                qr_code.make(fit=True)
                temp = BytesIO()
                qr_code.make_image().save(temp, format="PNG")
                employee.qr_code = BinaryBytes(temp.getvalue())
            else:
                employee.qr_code = False
