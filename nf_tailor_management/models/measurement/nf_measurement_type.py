from odoo import models, fields

class MeasurementType(models.Model):
    _name = 'nf.measurement.type'
    _description = 'Measurement Type'

    name = fields.Char(string="Measurement Type", required=True)
    code = fields.Char(string="Code")
    active = fields.Boolean(string="Active", default=True)
