# nf_measurement/models/measurement_category.py
from odoo import models, fields

class MeasurementCategory(models.Model):
    _name = 'nf.measurement.category'
    _description = 'Measurement Category'

    name = fields.Char(string="Category Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    measurement_line_ids = fields.One2many('nf.measurement.line', 'measurement_category_id')
    gender = fields.Selection([('male', 'Male'), ('female','Female'), ('other','Other')], required=True, default="male")
    measurement_design_ids = fields.One2many('nf.measurement.design', 'measurement_category_id')