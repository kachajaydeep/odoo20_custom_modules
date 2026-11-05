from odoo import models, fields, api

class NFDesignline(models.Model):
    _name = 'nf.design.line'
    _description = 'NF Design line'
    

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    image_1920 = fields.Image(string="Image", max_width=128, max_height=128)
    design_id = fields.Many2one('nf.design.type',string='Design',)

