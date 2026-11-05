# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import fields,models
import json

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    nf_show_name = fields.Boolean(string="Show Product Name",config_parameter="nf_price_checker_kiosk.nf_show_name")
    nf_company_name = fields.Boolean(string="Show Company Name",config_parameter="nf_price_checker_kiosk.nf_company_name")
    nf_company_logo = fields.Boolean(string="Show Company logo",config_parameter="nf_price_checker_kiosk.nf_company_logo")
    nf_show_image = fields.Boolean(string="Show Product Image",config_parameter="nf_price_checker_kiosk.nf_show_image")
    nf_show_code = fields.Boolean(string="Show Product Code",config_parameter="nf_price_checker_kiosk.nf_show_code")
    nf_show_barcode = fields.Boolean(string="Show Barcode",config_parameter="nf_price_checker_kiosk.nf_show_barcode")
    nf_show_price = fields.Boolean(string="Show Price",config_parameter="nf_price_checker_kiosk.nf_show_price")
    nf_show_stock = fields.Boolean(string="Show Stock",config_parameter="nf_price_checker_kiosk.nf_show_stock")
    nf_show_specification = fields.Boolean(string="Show Specification",config_parameter="nf_price_checker_kiosk.nf_show_specification")
    nf_show_category = fields.Boolean(string="Show category",config_parameter="nf_price_checker_kiosk.nf_show_category")
    nf_show_keyboard = fields.Boolean(string="Show Keyboard",config_parameter="nf_price_checker_kiosk.nf_show_keyboard")
    nf_show_product_weight = fields.Boolean(string="Show Product Weight",config_parameter="nf_price_checker_kiosk.nf_show_product_weight")
    nf_show_product_sales_description = fields.Boolean(string="Show Product Sale Description",config_parameter="nf_price_checker_kiosk.nf_show_product_sales_description")
    nf_show_product_tax = fields.Boolean(string="Show Product Tax",config_parameter="nf_price_checker_kiosk.nf_show_product_tax")
    nf_show_pricelist = fields.Boolean(string="Show Pricelist Price",config_parameter="nf_price_checker_kiosk.nf_show_pricelist")
    nf_pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        string="Kiosk Pricelists",
        relation="nf_kiosk_pricelist_rel",
    )
    
    def get_values(self):
        res = super().get_values()
        param = self.env['ir.config_parameter'].sudo().get_str(
            'nf_price_checker_kiosk.nf_pricelist_ids' , '[]'
        )

        ids = [int(i) for i in param.split(',') if i.strip().isdigit()]


        res['nf_pricelist_ids'] = [(6, 0, ids)]
        return res
    
    # def set_values(self):
    #     super().set_values()
    #     ids_str = ','.join(str(i) for i in self.nf_pricelist_ids.ids)
    #     print("\n\n\n ids_str ???",ids_str)
    #     self.env['ir.config_parameter'].sudo().get_str(
    #         'nf_price_checker_kiosk.nf_pricelist_ids', ids_str
    #     )
    #     group = self.env.ref('nf_price_checker_kiosk.nf_price_checker_kiosk_privilege')
    #     if self.nf_show_configuration:
    #         self.env.user.write({'group_ids': [(4, group.id)]})  
    #     else:
    #         self.env.user.write({'group_ids': [(3, group.id)]})

    def set_values(self):
        super().set_values()

        ids_str = ",".join(str(i) for i in self.nf_pricelist_ids.ids)

        self.env["ir.config_parameter"].sudo().set_str(
            "nf_price_checker_kiosk.nf_pricelist_ids",
            ids_str,
        )

        group = self.env.ref(
            "nf_price_checker_kiosk.nf_price_checker_kiosk_privilege"
        )

        if self.nf_pricelist_ids:
            self.env.user.write({"group_ids": [(4, group.id)]})
        else:
            self.env.user.write({"group_ids": [(3, group.id)]})
        