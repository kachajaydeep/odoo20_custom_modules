# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields,api

class NfReceiptTemplate(models.Model):
    _name = 'nf.receipt.template'
    _inherit = ['pos.load.mixin']
    _description = 'Receipt Template'
    _rec_name = 'nf_receipt_name'

    nf_receipt_name = fields.Char(string="Name")
    nf_receipt_xml = fields.Text(string="Receipt XML")
    nf_view_id = fields.Many2one('ir.ui.view', string="Rendered View", readonly=True, copy=False, ondelete='cascade')


    @api.model
    def _load_pos_data_domain(self, data):
        return []
    
    @api.model
    def _load_pos_data_fields(self,config):
        return []
    
    def _load_pos_data_search_read(self,record,config):
        domain = self._load_pos_data_domain(record,config)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain,fields)
        return records

    # def _view_key(self):
    #     self.ensure_one()
    #     return f'nf_pos_custom_receipt.nf_receipt_template_{self.id}'

    # def _sync_view(self):
    #     for record in self:
    #         arch = f'<t t-name="{record._view_key()}">{record.nf_receipt_xml or ""}</t>'
    #         if record.nf_view_id:
    #             record.nf_view_id.arch_db = arch
    #         else:
    #             view = self.env['ir.ui.view'].create({
    #                 'name': record._view_key(),
    #                 'key': record._view_key(),
    #                 'type': 'qweb',
    #                 'arch_db': arch,
    #             })
    #             record.nf_view_id = view.id

    # @api.model_create_multi
    # def create(self, vals_list):
    #     records = super().create(vals_list)
    #     records._sync_view()
    #     return records

    # def write(self, vals):
    #     res = super().write(vals)
    #     if 'nf_receipt_xml' in vals:
    #         self._sync_view()
    #     return res

    # def unlink(self):
    #     views = self.nf_view_id
    #     res = super().unlink()
    #     views.unlink()
    #     return res

        