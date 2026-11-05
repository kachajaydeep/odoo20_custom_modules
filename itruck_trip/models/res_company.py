from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    arabic_name = fields.Char('Arabic Name')
    arabic_city = fields.Char('Arabic Name of City')
