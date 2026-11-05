# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api, _

class MrpBom(models.Model):
    _name = "nf.mrp.bom"
    _inherit = "pos.load.mixin"

    name = fields.Char(
        string="Name", default=lambda self: _("New"), readonly=True, copy=False
    )
    nf_bom_component_ids = fields.One2many(
        "nf.bom.component", "nf_mrp_bom_id", string="Bom Components"
    ) 

    @api.model_create_multi
    def create(self, vals_list):
        for create_new_bom in vals_list:
            if create_new_bom.get("name", _("New")) == _("New"):
                create_new_bom["name"] = self.env["ir.sequence"].next_by_code(
                    "nf.mrp.bom"
                )
        return super(MrpBom, self).create(vals_list)
        
    @api.model
    def _load_pos_data_domain(self, data):
        return []

    @api.model
    def _load_pos_data_fields(self, config):
        return []

    def _load_pos_data_search_read(self, data, config):
        domain = self._load_pos_data_domain(data)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain, fields)
        return records

    def action_confirm(self):
        self.ensure_one()

        if self.nf_bom_component_ids and self.nf_bom_component_ids[0].bom_id:
            bom_lines = self.nf_bom_component_ids[0].bom_id.bom_line_ids
            for comp_line in self.nf_bom_component_ids:
                matching_bom_lines = bom_lines.filtered(lambda b: b.product_id == comp_line.product_id)
                for bom_line in matching_bom_lines:
                    bom_line.write({
                        'product_qty': comp_line.product_qty
                    })

        return {
            "type": "ir.actions.act_window_close",
        }


class MrpBomLine(models.Model):
    _name = "mrp.bom.line"
    _inherit = ["pos.load.mixin","mrp.bom.line"]
    _description = "Bill of Material Line"

    @api.model
    def _load_pos_data_domain(self, data):
        return []

    @api.model
    def _load_pos_data_fields(self, config):
        return []

    def _load_pos_data_search_read(self, data, config):
        domain = self._load_pos_data_domain(data)
        fields = self._load_pos_data_fields(config)
        records = self.search_read(domain, fields)
        return records
