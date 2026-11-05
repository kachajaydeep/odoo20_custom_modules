from odoo import models, fields, api

class DesignType(models.Model):
    _name = 'nf.design.type'
    _description = 'Design Type'

    name = fields.Char('Design Type Name', required=True)
    active = fields.Boolean('Active', default=True)
    design_line_ids = fields.One2many('nf.design.line', 'design_id')