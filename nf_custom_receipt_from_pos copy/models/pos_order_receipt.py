# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.
from odoo import models, fields

class PosOrderReceipt(models.AbstractModel):
    _inherit = 'pos.order.receipt'

    def order_receipt_generate_data(self, basic_receipt=False):
        data = super().order_receipt_generate_data(basic_receipt)
        config = self.config_id

        if(config.nf_receipt_template_id and config.nf_custom_receipt_template):
            data['extra_data']['nf_custom_receipt_template_name'] = (
                f'nf_pos_custom_receipt.nf_receipt_template_{config.nf_receipt_template_id.id}'
            )
        else:
            data['extra_data']['nf_custom_receipt_template_name'] = False
            
        return data
