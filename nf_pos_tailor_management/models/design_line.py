# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api, _


class NFDesignline(models.Model):
    _name = "nf.design.line"
    _inherit = ["pos.load.mixin","nf.design.line"]

    @api.model
    def _load_pos_data_domain(self, data):
        return []

    @api.model
    def _load_pos_data_fields(self, config):
        return []

    def _load_pos_data_search_read(self, data, config):
        domain = self._load_pos_data_domain(data)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain, fields)
        return records
