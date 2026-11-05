from odoo import fields, models, _
from odoo.exceptions import ValidationError


class TripCancelBy(models.TransientModel):
    _name = 'trip.cancel.by'

    trip_ids = fields.Many2many('itruck.trip', string='Trip', required=True)
    canceled_by = fields.Selection([
        ('by_shipper', 'Canceled by Shipper'),
        ('by_driver', 'Canceled by Driver')], string='Canceled By', required=True)

    def action_cancel_trip(self):
        for trip_id in self.trip_ids:
            if trip_id.invoice_id:
                if trip_id.invoice_id.payment_state in ['paid', 'partial']:
                    raise ValidationError(_('The Payment is already has been created, \n '
                                            'if you want to cancel the trip, Cancel the Payment of the Invoice first!'))
                # else:
                #     trip_id.invoice_id.button_cancel()
            if trip_id.bill_id:
                if trip_id.bill_id.payment_state in ['paid', 'partial']:
                    raise ValidationError(_('The Payment is already has been created, \n '
                                            'if you want to cancel the trip, Cancel the Payment of the Bill first!'))
                else:
                    trip_id.bill_id.button_cancel()
            trip_id.write({'state': 'cancel', 'canceled_by': self.canceled_by})
