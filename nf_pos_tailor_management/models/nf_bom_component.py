# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api

class NfMrpProduction(models.Model):
    _name = "nf.bom.component"
    _inherit = ["mrp.bom.line","pos.load.mixin"]
    _descrition = "Nf Bom Component"

    nf_pos_order_line_id = fields.Many2one("pos.order.line", string="Pos Order Line")
    nf_mrp_bom_id = fields.Many2one("nf.mrp.bom", string="Componenet Line")

    @api.model
    def _load_pos_data_domain(self, data):
        return []

    @api.model
    def _load_pos_data_fields(self, config):
        return ["nf_pos_order_line_id", "nf_mrp_bom_id", "bom_id"]

    def _load_pos_data_search_read(self, data, config):
        domain = self._load_pos_data_domain(data)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain, fields)
        return records