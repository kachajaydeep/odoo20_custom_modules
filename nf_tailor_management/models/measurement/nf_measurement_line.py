
from odoo import models, fields

class MeasurementLine(models.Model):
    _name = 'nf.measurement.line'
    _description = 'Measurement Line'

    measurement_id = fields.Many2one(comodel_name='nf.measurement', string='measurement')
    size = fields.Float(string='Size', required=True)
    note = fields.Text(string='Note')
    tailor_order_id  = fields.Many2one('nf.tailor.order', string="tailor order")
    measurement_category_id = fields.Many2one('nf.measurement.category', string='Measurement Category')
    measurement_type_id = fields.Many2one(comodel_name='nf.measurement.type', string='Type')
    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Type')