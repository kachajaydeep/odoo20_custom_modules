from odoo import models, fields, api, Command

class Measurement(models.Model):
    _name = 'nf.measurement'
    _description = 'Measurement Model'

    name = fields.Char(string='Name', required=True)
    uom_id = fields.Many2one('uom.uom',string='Uom')
    active = fields.Boolean("Active", default=True)
    gender = fields.Selection([('male', 'Male'), ('female','Female'), ('other','Other')], required=True)
    measurement_categ_id = fields.Many2one('nf.measurement.category', string='Category',) 
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    measurement_line_ids = fields.One2many(comodel_name='nf.measurement.line', inverse_name='measurement_id', string='Measurement Lines') 
    measurement_design_ids = fields.One2many('nf.measurement.design', 'measurement_id', )

    @api.onchange('measurement_categ_id')
    def onchange_measurement_categ_id(self):
        self.measurement_line_ids = [Command.clear()] + [Command.create(line_vals) for line_vals in self.measurement_categ_id.measurement_line_ids.read(load=False)]
        self.measurement_design_ids = [Command.clear()] + [Command.create(line_vals) for line_vals in self.measurement_categ_id.measurement_design_ids.read(load=False)]
    
    @api.onchange('gender')
    def onchange_gender(self):
        self.measurement_categ_id = False
    
