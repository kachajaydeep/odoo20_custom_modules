from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TripAccounting(models.TransientModel):
    _name = 'trip.account.move'

    trip_ids = fields.Many2many('itruck.trip', string='Trips', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    move_id = fields.Many2one('account.move', 'Invoice/Bill')
    need_to_create_separate_move = fields.Boolean("Need to create separate Invoice?")
    move_type = fields.Selection([
        ('out_invoice', 'Invoice'),
        ('in_invoice', 'Bill')], string='Move Type')

    # def action_create_invoice(self):
    #     if not self.move_id:
    #         raise ValidationError(_("Please select the Invoice first!!!"))
    #     analytic_account = self.env['account.analytic.account']
    #     move_id = self.move_id
    #     if not move_id:
    #         move_id = self.move_id.create({'move_type': 'out_invoice', 'partner_id': self.partner_id.id})
    #     move_id = move_id.with_context(check_move_validity=False)
    #     for product_id in self.trip_ids.product_id:
    #         trip_ids = self.trip_ids.filtered(lambda t: t.product_id == product_id)
    #
    #         analytic_account_name = f"{product_id.loading_point.name}-{product_id.unloading_point.name}"
    #         analytic_account_id = analytic_account.search([('name', 'ilike', analytic_account_name)], limit=1)
    #         if not analytic_account_id:
    #             analytic_account_id = analytic_account.create({'name': analytic_account_name})
    #
    #         # if trip_id.bill_id:
    #         #     trip_id.action_done()
    #
    #         available_lines = move_id.invoice_line_ids.filtered(lambda l: l.product_id == product_id)
    #         if available_lines and not self._context.get('create_from_form'):
    #             available_lines[0].write({'quantity': available_lines[0].quantity + len(trip_ids)})
    #         else:
    #             vals = {
    #                 'product_id': product_id.id,
    #                 'tax_ids': product_id.taxes_id.ids if product_id.taxes_id else False,
    #                 'analytic_account_id': analytic_account_id.id,
    #                 'quantity': len(trip_ids),
    #                 'price_unit': trip_ids[0].amount,
    #                 # 'account_id': self.company_data['default_account_revenue'].id,
    #             }
    #             if len(trip_ids) == 1:
    #                 trip_id = trip_ids[0]
    #                 vals.update({
    #                     'price_unit': trip_id.amount,
    #                     'trip_date': trip_id.date,
    #                     'trip_id': trip_id.id,
    #                     'fleet_id': trip_id.fleet_id.id if trip_id.fleet_id else False,
    #                     'dn_number': trip_id.dn_number})
    #             move_id.write({'invoice_line_ids': [(0, 0, vals)]})
    #         for trip_id in trip_ids:
    #             if trip_id.bill_id:
    #                 trip_id.action_done()
    #             trip_id.write({'invoice_id': move_id.id, 'state': 'invoiced'})
    #     if sum(move_id.line_ids.mapped('credit')) != sum(move_id.line_ids.mapped('debit')):
    #         lines = move_id.line_ids.filtered(lambda l: l.account_id and l.account_id.user_type_id.type == 'receivable')
    #         if lines:
    #             debit = sum(move_id.line_ids.mapped('credit')) - sum(move_id.line_ids.mapped('debit'))
    #             lines[0].write({'debit': debit + sum(move_id.line_ids.mapped('debit'))})
    #
    #     action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
    #     action['domain'] = [('id', '=', move_id.id)]
    #     form_view = [(self.env.ref('account.view_move_form').id, 'form')]
    #     if 'views' in action:
    #         action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
    #     else:
    #         action['views'] = form_view
    #     action['res_id'] = move_id.id
    #
    #     context = {
    #         'default_move_type': 'out_invoice',
    #     }
    #     action['context'] = context
    #     return action

    def action_create_invoice(self):
        if not self.need_to_create_separate_move:
            if not self.move_id:
                raise ValidationError(_("Please select the Invoice first!!!"))
            analytic_account = self.env['account.analytic.account']
            move_id = self.move_id
            if not move_id:
                move_id = self.move_id.create({'move_type': 'out_invoice', 'partner_id': self.partner_id.id})
            move_id = move_id.with_context(check_move_validity=False)
            for trip_id in self.trip_ids.filtered(lambda t: t.id not in move_id.invoice_line_ids.trip_id.ids):
                # analytic_account_name = f"{trip_id.loading_point.name}-{trip_id.unloading_point.name}"
                # analytic_account_id = analytic_account.search([('name', 'ilike', analytic_account_name)], limit=1)
                # if not analytic_account_id:
                #     analytic_account_id = analytic_account.create({'name': analytic_account_name})

                product_id = trip_id.product_id
                line_vals = {
                     'product_id': product_id.id,
                     'tax_ids': product_id.taxes_id.ids if product_id.taxes_id else False,
                     # 'analytic_account_id': analytic_account_id.id,
                     'quantity': 1.0,
                     'price_unit': trip_id.amount,
                     # 'account_id': self.company_data['default_account_revenue'].id,
                     'trip_date': trip_id.date,
                     'trip_id': trip_id.id,
                     'fleet_id': trip_id.fleet_id.id if trip_id.fleet_id else False,
                     'dn_number': trip_id.dn_number
                }
                if trip_id.monthly_rent:
                    line_vals.update({'account_id': self.env.ref('l10n_sa.1_sa_account_500002').id})
                move_id.write({'invoice_line_ids': [(0, 0, line_vals)]})
                if trip_id.bill_id:
                    trip_id.action_done()
                trip_id.write({'invoice_id': move_id.id, 'state': 'invoiced'})
            if sum(move_id.line_ids.mapped('credit')) != sum(move_id.line_ids.mapped('debit')):
                lines = move_id.line_ids.filtered(lambda l: l.account_id and l.account_id.user_type_id.type == 'receivable')
                if lines:
                    debit = sum(move_id.line_ids.mapped('credit')) - sum(move_id.line_ids.mapped('debit'))
                    lines[0].write({'debit': debit + sum(move_id.line_ids.mapped('debit'))})

            action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
            action['domain'] = [('id', '=', move_id.id)]
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = move_id.id

            context = {
                'default_move_type': 'out_invoice',
            }
            action['context'] = context
            return action
        else:
            analytic_account = self.env['account.analytic.account']
            for trip_id in self.trip_ids:
                move_id = self.move_id.create({'move_type': 'out_invoice', 'partner_id': self.partner_id.id})
                move_id = move_id.with_context(check_move_validity=False)
                # analytic_account_name = f"{trip_id.loading_point.name}-{trip_id.unloading_point.name}"
                # analytic_account_id = analytic_account.search([('name', 'ilike', analytic_account_name)], limit=1)
                # if not analytic_account_id:
                #     analytic_account_id = analytic_account.create({'name': analytic_account_name})

                product_id = trip_id.product_id
                line_vals = {
                    'product_id': product_id.id,
                    'tax_ids': product_id.taxes_id.ids if product_id.taxes_id else False,
                    # 'analytic_account_id': analytic_account_id.id,
                    'quantity': 1.0,
                    'price_unit': trip_id.amount,
                    # 'account_id': self.company_data['default_account_revenue'].id,
                    'trip_date': trip_id.date,
                    'trip_id': trip_id.id,
                    'fleet_id': trip_id.fleet_id.id if trip_id.fleet_id else False,
                    'dn_number': trip_id.dn_number
                }
                if trip_id.monthly_rent:
                    line_vals.update({'account_id': self.env.ref('l10n_sa.1_sa_account_500002').id})
                move_id.write({'invoice_line_ids': [(0, 0, line_vals)]})
                if trip_id.bill_id:
                    trip_id.action_done()
                trip_id.write({'invoice_id': move_id.id, 'state': 'invoiced'})

                if sum(move_id.line_ids.mapped('credit')) != sum(move_id.line_ids.mapped('debit')):
                    lines = move_id.line_ids.filtered(
                        lambda l: l.account_id and l.account_id.user_type_id.type == 'receivable')
                    if lines:
                        debit = sum(move_id.line_ids.mapped('credit')) - sum(move_id.line_ids.mapped('debit'))
                        lines[0].write({'debit': debit + sum(move_id.line_ids.mapped('debit'))})

            action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
            action['domain'] = [('id', 'in', self.trip_ids.invoice_id.ids)]
            action['views'] = [(self.env.ref('account.view_out_invoice_tree').id, 'list'),
                               (self.env.ref('account.view_move_form').id, 'form')]
            context = {'default_move_type': 'out_invoice'}
            action['context'] = context
            return action

    def action_create_bill(self):
        if not self.move_id:
            raise ValidationError(_("Please select the Bill first!!!"))
        analytic_account = self.env['account.analytic.account']
        for trip_id in self.trip_ids.filtered(lambda t: t.id not in self.move_id.invoice_line_ids.trip_id.ids):
            # analytic_account_name = f"{trip_id.loading_point.name}-{trip_id.unloading_point.name}"
            # analytic_account_id = analytic_account.search([('name', 'ilike', analytic_account_name)], limit=1)
            # if not analytic_account_id:
            #     analytic_account_id = analytic_account.create({'name': analytic_account_name})

            if trip_id.invoice_id:
                trip_id.action_done()
            vals = {'invoice_line_ids': [(0, 0, {
                'product_id': trip_id.product_id.id,
                'tax_ids': trip_id.product_id.supplier_taxes_id.ids if trip_id.product_id.supplier_taxes_id else False,
                'price_unit': trip_id.carrier_amount,
                # 'analytic_account_id': analytic_account_id.id,
                'trip_date': trip_id.date,
                'quantity': 1,
                'trip_id': trip_id.id,
                'fleet_id': trip_id.fleet_id.id if trip_id.fleet_id else False,
                'dn_number': trip_id.dn_number,
                # 'account_id': self.company_data['default_account_revenue'].id,
            })]}
            if self.move_id:
                if trip_id.id not in self.move_id.invoice_line_ids.trip_id.ids:
                    self.move_id.write(vals)
                move_id = self.move_id
            else:
                vals.update({'move_type': 'in_invoice',
                             'partner_id': self.partner_id.id,
                             'date': trip_id.date, })
                move_id = self.move_id.create(vals)
            if move_id:
                trip_id.write({'bill_id': move_id.id})
        return True
