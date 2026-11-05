# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    pos_session_id = fields.Many2one("pos.session", string="POS Session", copy=False)
    employee_id = fields.Many2one("hr.employee", string="Requested By", copy=False)

    @api.model
    def create_from_pos_ui(self, values, po_status, validate_po_receipt, create_bill):
        if values.get("employee_id") == False:
            employee_id = self.env["hr.employee"].search(
                [("user_id", "=", self.env.uid)], limit=1
            )
            values.update({"employee_id": employee_id.id})
        values.update({"partner_id": int(values["partner_id"])})
        purchase = self.create(values)
        purchase.order_line._compute_tax_id()
        purchase._auto_flow_from_pos(po_status, validate_po_receipt, create_bill)
        return {"name": purchase.name, "id": purchase.id}

    def _auto_flow_from_pos(self, po_status, validate_po_receipt, create_bill):
        if po_status == "sent":
            action = self.action_rfq_send()
            if action["res_model"] == "base.document.layout":
                return action
            rec = (
                self.env[action["res_model"]].with_context(action["context"]).create({})
            )
            rec.action_send_mail()
        elif po_status == "purchase":
            self.button_confirm()
            if validate_po_receipt:
                for picking in self.picking_ids:
                    picking.action_assign()
                    picking.button_validate()
                if create_bill:
                    self.action_create_invoice()