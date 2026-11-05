# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import fields,models,api,_
from odoo.exceptions import UserError 

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    nf_pos_config_id = fields.Many2one("pos.config", string="POS Config")
    
    @api.model
    def _load_pos_data_domain(self, data,config):
        return []
    
    def _load_pos_data_fields(self,config):
        return []
    
    def _load_pos_data_search_read(self, data, config):
        domain = self._load_pos_data_domain(data,config)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain,fields)
        return records
    
    @api.model
    def create_from_pos(self):
        stock_move = []
        picking_ctx = self.env.context.get('pickingcontext')
        move_ctx = self.env.context.get('stock_move_context')
        product = self.env['product.product'].browse(move_ctx['product_id'])


        stock_move.append((0,0,{
            'product_id': product.id,
            'product_uom_qty': move_ctx['product_uom_qty'],
            'uom_id': product.uom_id.id,
            'location_id': picking_ctx['location_id'],
            'location_dest_id': picking_ctx['location_dest_id'],
            }))
        picking_ctx['move_ids'] = stock_move
        if not picking_ctx.get('picking_type_id'):
            internal_picking_type = self.env['stock.picking.type'].search([
                ('code', '=', 'internal')
            ], limit=1)
            picking_ctx['picking_type_id'] = internal_picking_type.id

        picking = self.create(picking_ctx)
        self._notify_stock_request(picking)
        return picking.id
    
    def _notify_stock_request(self, picking):
        """Send a real-time notification to POS sessions that 'own' the source location."""
        source_location_id = picking.location_id.id
        
        target_configs = self.env['pos.config'].search([
            ('picking_type_id.default_location_src_id', '=', source_location_id)
        ])
        
        if not target_configs:
            return
        
        product_name = (
            picking.move_ids[0].product_id.display_name
            if picking.move_ids else "Unknown Product"
        )

        for config in target_configs:
            config._notify("ST_REQUEST_ARRIVE", {
                'id': picking.id,
                'move_id': picking.move_ids[0].id if picking.move_ids else False,
                'picking_id': [picking.id, picking.name],
                'product_name': product_name,
                'location_id': [picking.location_id.id, picking.location_id.display_name],
                'location_dest_id': [picking.location_dest_id.id, picking.location_dest_id.display_name],
                'origin_pos': picking.nf_pos_config_id.name or "Another POS",
                'state': picking.state,
            })
            
    @api.model
    def action_validate_from_pos(self, picking_id, move_data):
        """Validate a picking from POS using the provided move quantities."""
        
        if not self.env.user.has_group('stock.group_stock_manager'):
            raise UserError(_("Only Inventory Administrators can approve stock requests."))
        picking = self.browse(picking_id)

        if not picking:
            return False
        
        if picking.state not in ('assigned', 'done', 'cancel'):
            picking.action_assign()
            
        for move_item in move_data:
            move = self.env['stock.move'].browse(move_item['id'])
            if move and move.picking_id == picking:
                move.quantity = float(move_item['quantity'])
        
        res = picking.button_validate()
        
        if isinstance(res, dict) and res.get('res_model') in ['stock.backorder.confirmation', 'stock.immediate.transfer']:
            wizard_model = res['res_model']
            wizard = self.env[wizard_model].with_context(res['context']).create({})
            if hasattr(wizard, 'process'):
                wizard.process()
            elif hasattr(wizard, 'action_create_backorder'):
                wizard.action_create_backorder()
            self._notify_stock_approved(picking)
            return True

        self.env['bus.bus']._sendone(
            "nf_pos_stock_request_channel", 
            "stock_picking_validated",
            {"picking_id": self.id}
        )
        
        self._notify_stock_approved(picking)
        return True

    
    def _notify_stock_approved(self, picking):
        """Notify the requesting POS (nf_pos_config_id) that their stock request was approved."""
        product = picking.move_ids[0].product_id if picking.move_ids else False
        if not product:
            return

        requesting_config = picking.nf_pos_config_id
        if requesting_config:
            req_qty = self.env['stock.quant'].get_product_quantity_for_pos(requesting_config, product.id)
            requesting_config._notify("ST_REQUEST_APPROVED", {
                'id': picking.id,
                'picking_id': [picking.id, picking.name],
                'product_name': product.display_name,
                'state': picking.state,
                'approved_by': self.env.user.name,
                'product_id': product.id,
                'quantity': req_qty,
                'is_requester': True,
            })

        fulfilling_configs = self.env['pos.config'].search([
            ('picking_type_id.default_location_src_id', '=', picking.location_id.id)
        ])
        for config in fulfilling_configs:
            if config == requesting_config:
                continue
            ful_qty = self.env['stock.quant'].get_product_quantity_for_pos(config, product.id)
            config._notify("ST_REQUEST_APPROVED", {
                'id': picking.id,
                'picking_id': [picking.id, picking.name],
                'product_name': product.display_name,
                'state': picking.state,
                'approved_by': self.env.user.name,
                'approve_id':self.env.user,
                'product_id': product.id,
                'quantity': ful_qty,
                'change_qty': -picking.move_ids[0].product_uom_qty,
                'is_requester': False,
            })
        
        
        configs = self.env['pos.config'].search([
        '|',
        ('picking_type_id.default_location_src_id', '=', picking.location_id.id),
        ('picking_type_id.default_location_src_id', '=', picking.location_dest_id.id),
        ])

        payload = {
            'picking_id': [picking.id, picking.name],
            'product_name': picking.move_ids[0].product_id.display_name if picking.move_ids else '',
            'approved_by': self.env.user.name,
        }

        for config in configs:
            config._notify("APPROVE-RECORD-FROM-ANOTHER-USER", payload)