from odoo import api, models, fields, _
from odoo.osv import expression


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    trip_date = fields.Date(string='Trip Date')
    trip_id = fields.Many2one('itruck.trip')
    fleet_id = fields.Many2one('fleet.vehicle', string='Plate No.')
    dn_number = fields.Char('D/N No.')


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if operator == 'ilike':
            domain = [('display_name', 'ilike', name)]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super()._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    def _check_balanced(self, container):
        ''' Assert the move is fully balanced debit = credit.
        An error is raised if it's not the case.
        '''
        if not self._context.get('pass_check_balanced', False):
            return super(AccountMove, self)._check_balanced(container=container)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if operator == 'ilike':
            domain = [('ref', 'ilike', name)]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super()._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    @api.onchange('partner_id')
    def onchange_for_salesperson_and_team(self):
        if self.partner_id:
            self.invoice_user_id = self.partner_id.user_id.id if self.partner_id.user_id else False
            self.team_id = self.partner_id.team_id.id if self.partner_id.team_id else False
