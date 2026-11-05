from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    sale_team_leader_ids = fields.One2many('crm.team', 'user_id', string='User Sales Leader Team',
                                           compute='_compute_sale_team_leader_ids', readonly=True)

    def _compute_sale_team_leader_ids(self):
        for user in self:
            user.sale_team_leader_ids = self.env['crm.team'].search([('user_id', '=', user.id)]).ids or False
