from odoo import fields, models, _
from odoo.exceptions import ValidationError


class DuplicateTrip(models.TransientModel):
    _name = 'duplicate.trip'

    trip_id = fields.Many2one('itruck.trip', 'Trip', required=True)
    number_of_duplication = fields.Integer('Number of Duplications', default=10, required=True)

    def action_create_duplicate_trips(self):
        vals = []
        trip_id = self.trip_id
        if trip_id.partner_id.blacklisted:
            raise ValidationError(_("The Shipper '%s' is Blacklisted!" % trip_id.partner_id.name))
        for duplicate_trip in range(self.number_of_duplication):
            vals.append({
                'partner_id': trip_id.partner_id.id,
                'shipper_fleet_type': trip_id.shipper_fleet_type,
                'consignee_id': trip_id.consignee_id.id if trip_id.consignee_id else False,
                'consignee_phone': trip_id.consignee_phone,
                'tag_ids': trip_id.tag_ids.ids,
                'product_id': trip_id.product_id.id,
                'date': trip_id.date,
                'user_id': trip_id.user_id.id,
                'product_type_id': trip_id.product_type_id.id,
                'weight': trip_id.weight,
                'amount': trip_id.amount,
                'carrier_amount': trip_id.carrier_amount,
                'target_amount': trip_id.target_amount,
            })
        duplicate_trips = self.trip_id.create(vals)
        return {
            'name': _('Duplicated Trips'),
            'view_mode': 'list,form',
            'res_model': 'itruck.trip',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', duplicate_trips.ids)],
        }
