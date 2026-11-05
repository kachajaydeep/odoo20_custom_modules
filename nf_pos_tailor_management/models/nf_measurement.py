# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api


class Measurement(models.Model):
    _name = "nf.measurement"
    _inherit = ["pos.load.mixin","nf.measurement"]

    @api.model
    def _load_pos_data_domain(self, data):
        return []

    @api.model
    def _load_pos_data_fields(self, config):
        # return ["create_date","display_name","gender","id","measurement_categ_id","measurement_design_ids","measurement_line_ids","name","partner_id","uom_id"]
        return [
            "id",
            "create_date",
            "display_name",
            "gender",
            "measurement_categ_id",
            "measurement_design_ids",
            "measurement_line_ids",
            "name",
            "partner_id",
            "uom_id",
            "write_date",
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
