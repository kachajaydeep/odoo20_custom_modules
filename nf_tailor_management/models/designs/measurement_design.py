# nf_measurement/models/measurement_category.py
from odoo import models, fields

class MeasurementCategory(models.Model):
    _name = 'nf.measurement.design'
    _description = 'Measurement design'
    _rec_name = 'design_type'

    design_type = fields.Many2one('nf.design.type', string="Design type")
    design_image = fields.Many2one('nf.design.line', string="Design Image")
    image_1920 = fields.Image(related="design_image.image_1920", max_width=128, max_height=128)
    measurement_category_id = fields.Many2one('nf.measurement.category', string="Measurement category")
    tailor_order_id = fields.Many2one('nf.tailor.order', string="Tailor Order")
    measurement_id = fields.Many2one(comodel_name='nf.measurement', string='measurement')


    

    