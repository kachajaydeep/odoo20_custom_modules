from odoo import models, fields, api


class MeasurementType(models.Model):
    _name = "nf.measurement.type"
    _inherit = ["pos.load.mixin","nf.measurement.type"]
    _description = "Nf Measurement Type"

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
