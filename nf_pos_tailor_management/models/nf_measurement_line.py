# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api


class MeasurementLine(models.Model):
    _name = "nf.measurement.line"
    _inherit = ["pos.load.mixin","nf.measurement.line"]
    _description = "Nf Measurement Line"

    @api.model
    def _load_pos_data_domain(self, data):
        return []

    @api.model
    def _load_pos_data_fields(self, config):
        return [
            "id",
            "measurement_type_id",
            "size",
            "note",
            "measurement_id",
            "tailor_order_id",
        ]

    def _load_pos_data_search_read(self, data, config):
        domain = self._load_pos_data_domain(data)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain, fields)
        return records

    @api.model
    def _load_pos_data_read(self, records, config):
        fields = self._load_pos_data_fields(config)
        return records.read(fields, load=False)
