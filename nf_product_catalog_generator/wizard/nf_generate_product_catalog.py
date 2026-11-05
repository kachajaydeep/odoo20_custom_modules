# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class GenerateProductCatolog(models.TransientModel):
    _name = 'nf.generate.product.catalog.wizard' # type: ignore
    _description = 'Generate Product Catalog'
    _inherit = 'nf.generated.product.catalog' # type: ignore
    
    catalog_record_id = fields.Many2one('nf.generated.product.catalog', string='Generated Catalog', readonly=True)

    def generate_pdf_report(self):
        self._validate_catalog_fields()
        catalog = self._create_catalog_record()
        report_map = {
            'style1': 'nf_product_catalog_generator.action_generate_pdf_report_style1',
            'style2': 'nf_product_catalog_generator.action_generate_pdf_report_style2',
            'style3': 'nf_product_catalog_generator.action_generate_pdf_report_style3',
            'style4': 'nf_product_catalog_generator.action_generate_pdf_report_style4',
            'style5': 'nf_product_catalog_generator.action_generate_pdf_report_style5',
        }
        xml_id = report_map.get(self.style, report_map['style1'])  # type: ignore
        report_action = self.env.ref(xml_id).report_action(catalog) # type: ignore
        report_action['close_on_report_download'] = True
        return report_action

    def generate_xls_report(self):
        """Create catalog record and immediately generate XLS."""
        self._validate_catalog_fields()
        catalog = self._create_catalog_record()
        result = catalog.download_xls_report()  # type: ignore
        self._success(result)
        return result

    def _validate_catalog_fields(self):
        """Centralized validation before creating anything."""
        if not self.catalog_name:   # type: ignore
            raise ValidationError("Catalog Name is required.")
        if not self.style:  # type: ignore
            raise ValidationError("Please select a Style before generating the report.")
        if not self.currency_id:    # type: ignore
            raise ValidationError("Currency is required.")
        if self.catalog_type == 'product' and not self.product_id:  # type: ignore
            raise ValidationError("Please select at least one product.")
        if self.catalog_type == 'category' and not self.category_id:    # type: ignore
            raise ValidationError("Please select a category.")

    def _create_catalog_record(self):
        """Create and return the catalog record from wizard fields."""

        cata_log_id = self.env['nf.generated.product.catalog'].create({
            'catalog_name':         self.catalog_name,                      # type: ignore
            'catalog_type':         self.catalog_type,                      # type: ignore
            'product_id':           [(6, 0, self.product_id.ids)],          # type: ignore
            'category_id':          self.category_id.id if self.category_id else False,  # type: ignore
            'print_category':       self.print_category,                     # type: ignore
            'image':                self.image,                             # type: ignore
            'image_height':         self.image_height,                      # type: ignore
            'image_width':          self.image_width,                       # type: ignore
            'currency_id':          self.currency_id.id if self.currency_id else False,  # type: ignore
            'price':                self.price,                             # type: ignore
            'pricelist':            self.pricelist.id if self.pricelist else False,      # type: ignore
            'price_decimal':        self.price_decimal,                     # type: ignore
            'style':                self.style,                             # type: ignore
            'printbox_per_row':     self.printbox_per_row,                  # type: ignore
            'description':          self.description,                       # type: ignore
            'product_link':         self.product_link,                      # type: ignore
            'inter_ref':            self.inter_ref,                         # type: ignore
            'print_uom':            self.print_uom,                         # type: ignore
            'break_page':           self.break_page,                        # type: ignore
            'break_after_product':  self.break_after_product,               # type: ignore
        })

        return cata_log_id
    
    @api.onchange('category_id')
    def _onchange_category_id(self):
        if self.category_id: # type: ignore
            all_category_ids = self.env['product.category'].search([
                ('id', 'child_of', self.category_id.id) # type: ignore
            ]).ids
            products = self.env['product.product'].search([
                ('categ_id', 'in', all_category_ids)
            ])
            self.product_id = [(6, 0, products.ids)]
        else:
            self.product_id = [(5, 0, 0)]
            
    # To refresh the 'Generated Catalog' page after creating PDF or XLS
    def _success(self, report_action):
        report_action['params'] = {
        'next': {
            'type': 'ir.actions.act_window',
            'res_model': 'nf.generated.product.catalog',
            'view_mode': 'list,form',
            'target': 'current',
        }
    }
   