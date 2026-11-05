from odoo import api, fields, models, _


class TripCity(models.Model):
    _name = "trip.city"
    _description = "Trip City"
    _rec_name = "name"

    name = fields.Char('City Name', required=True, translate=True)
    code = fields.Char('City Code', required=True, default='NEW', readonly=True)

    @api.model
    def create(self, values):
        values['code'] = self.env['ir.sequence'].next_by_code('trip.city')
        return super(TripCity, self).create(values)
