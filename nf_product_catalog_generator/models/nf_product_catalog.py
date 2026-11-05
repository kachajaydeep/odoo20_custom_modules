# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

import base64
import io
import xlsxwriter
from odoo.tools import html2plaintext
from bs4 import BeautifulSoup
from odoo import _, models, fields, api
from PIL import Image as PILImage

class GeneratedProductCatalog(models.Model):
    _name = 'nf.generated.product.catalog'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Generated Product Catalog'
    _rec_name = 'catalog_name'
    
    catalog_name = fields.Char(string='Catalog Name')
    product_id = fields.Many2many('product.product', string='Products')
    category_id = fields.Many2one('product.category', string='Categorys')
    print_category = fields.Boolean(string='Print Category ? ')
    image = fields.Boolean(string='Image')
    image_height = fields.Float(string='Height (in px)', default="100")
    image_width = fields.Float(string='Width (in px)', default="100")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id, required=True)
    price = fields.Boolean(string='Price', default=True)
    pricelist = fields.Many2one('product.pricelist', string='Pricelist')
    price_decimal = fields.Integer(string='Price Decimal Places')
    description = fields.Boolean(string='Description')
    product_link = fields.Boolean(string='Product Link')
    inter_ref = fields.Boolean(string='Internal Reference')
    print_uom = fields.Boolean(string='Print UOM ? ')
    break_page = fields.Boolean(string='Break Page', default=False)
    break_after_product = fields.Integer(string='Break page after products')
    
    catalog_type = fields.Selection([('product', 'Product'), ('category','Category')],default='product', string='Catalog Type') # type: ignore
    style = fields.Selection([('style1', 'Default'),('style2', 'Box'),('style3', 'Row'),('style4', 'Bubble'),('style5', 'Style 5')],default='style1', string='Style') #type: ignore
    printbox_per_row = fields.Selection([('2_box','2 box per row'),('3_box','3 box per row'),('4_box','4 box per row')],default='2_box', string='Print Box per Row') #type: ignore
    
    def send_email(self):
        mail_template = self.env['ir.model.data']._xmlid_to_res_id('nf_product_catalog_generator.product_catalog_email_template', raise_if_not_found=False)
        report_map_action = {
            'style1': 'nf_product_catalog_generator.action_generate_pdf_report_style1',
            'style2': 'nf_product_catalog_generator.action_generate_pdf_report_style2',
            'style3': 'nf_product_catalog_generator.action_generate_pdf_report_style3',
            'style4': 'nf_product_catalog_generator.action_generate_pdf_report_style4',
            'style5': 'nf_product_catalog_generator.action_generate_pdf_report_style5',
        }
        report_map_template = {
            'style1': 'nf_product_catalog_generator.report_product_catalog_style1',
            'style2': 'nf_product_catalog_generator.report_product_catalog_style2',
            'style3': 'nf_product_catalog_generator.report_product_catalog_style3',
            'style4': 'nf_product_catalog_generator.report_product_catalog_style4',
            'style5': 'nf_product_catalog_generator.report_product_catalog_style5',
        }
        xml_id = report_map_action.get(self.style, report_map_action['style1'])  # type: ignore
        template_id = report_map_template.get(self.style, report_map_template['style1'])  # type: ignore
        attachment_xls = self.generate_xls_report()
        attachment_pdf = self.generate_pdf_attachment(
            report_xml_id = xml_id,
            report_template_id= template_id,
            filename = f"{self.catalog_name} Report"
        )
        
        content_ctx = dict(
            default_model = 'nf.generated.product.catalog',
            default_template_id = mail_template,
            default_attachment_ids = [(4, attachment_xls.id),(4, attachment_pdf.id)]
        )
        return {
            'type': 'ir.actions.act_window',
            'name': _('Product Catalog Report Mail'),
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': content_ctx
        }
        
    def generate_pdf_report(self):
        report_map = {
            'style1': 'nf_product_catalog_generator.action_generate_pdf_report_style1',
            'style2': 'nf_product_catalog_generator.action_generate_pdf_report_style2',
            'style3': 'nf_product_catalog_generator.action_generate_pdf_report_style3',
            'style4': 'nf_product_catalog_generator.action_generate_pdf_report_style4',
            'style5': 'nf_product_catalog_generator.action_generate_pdf_report_style5',
        }
        xml_id = report_map.get(self.style, report_map['style1'])  # type: ignore
        return self.env.ref(xml_id).report_action(self) # type: ignore
            
    @api.onchange('category_id')
    def _onchange_category_id(self):
        if self.category_id: # type: ignore
            # Get current category + all child categories
            all_category_ids = self.env['product.category'].search([
                ('id', 'child_of', self.category_id.id) # type: ignore
            ]).ids
            products = self.env['product.product'].search([
                ('categ_id', 'in', all_category_ids)
            ])
            self.product_id = [(6, 0, products.ids)]
        else:
            self.product_id = [(5, 0, 0)]
        
    def generate_xls_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet("Catalog Report")

        row = 5
        report_name = self.catalog_name

        headers = ['Sr No.']
        col_map = {}  # maps field name to column index
        current_col = 1

        if self.image:
            headers.append('Image')
            col_map['image'] = current_col
            current_col += 1

        headers.append('Product Name')
        col_map['name'] = current_col
        current_col += 1

        if self.inter_ref:
            headers.append('Internal Reference')
            col_map['inter_ref'] = current_col
            current_col += 1

        headers.append('Product Type')
        col_map['type'] = current_col
        current_col += 1

        if self.print_category:
            headers.append('Category')
            col_map['category'] = current_col
            current_col += 1

        if self.print_uom:
            headers.append('UOM')
            col_map['uom'] = current_col
            current_col += 1

        if self.price:
            headers.append('Price')
            col_map['price'] = current_col
            current_col += 1

        if self.description:
            headers.append('Description')
            col_map['description'] = current_col
            current_col += 1

        total_cols = current_col  # total number of columns used

        # 🎨 Formats
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'font_size': 16,
            'bg_color': '#D9E1F2',
            'text_wrap': True
        })
        cell_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        text_format = workbook.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        })

        # 📏 Column widths
        worksheet.set_column(0, 0, 8)
        if 'image' in col_map:
            image_col_width = (self.image_width or 100) / 7
            worksheet.set_column(col_map['image'], col_map['image'], image_col_width)
        worksheet.set_column(col_map['name'], total_cols - 1, 18)

        worksheet.set_row(row - 4, 30)
        worksheet.merge_range(0, 0, 2, total_cols - 1, report_name, header_format)

        # Header row
        worksheet.set_row(row, 30)
        for col, head in enumerate(headers):
            worksheet.write(row, col, head, header_format)

        row += 2

        sr_no = 1
        for rec in self:
            for product in rec.product_id:  # type: ignore

                worksheet.set_row(row, 20)

                worksheet.write(row, 0, sr_no, cell_format)

                if self.image and 'image' in col_map:
                    if product.image_1920:  # type: ignore
                        print("\n\n\n product.image_1920",product.image_1920)
                        image_data = io.BytesIO(bytes(product.image_1920))  # type: ignore
                        
                        desired_width  = rec.image_width  or 100  # type: ignore
                        desired_height = rec.image_height or 100  # type: ignore

                        img = PILImage.open(io.BytesIO(bytes(product.image_1920)))  # type: ignore
                        actual_width, actual_height = img.size  # actual px dimensions

                        x_scale = desired_width  / actual_width
                        y_scale = desired_height / actual_height

                        worksheet.set_row(row, desired_height * 0.75)

                        image_data = io.BytesIO(bytes(product.image_1920))  # type: ignore

                        worksheet.insert_image(
                            row, col_map['image'], 'image.png',
                            {
                                'image_data':       image_data,
                                'x_scale':          x_scale,
                                'y_scale':          y_scale,
                                'x_offset':         5,
                                'y_offset':         5,
                                'positioning':      1,
                            }
                        )
                    else:
                        worksheet.write(row, col_map['image'], 'No Image', cell_format)

                worksheet.write(row, col_map['name'], product.display_name or 'Not Found', text_format)  # type: ignore

                if self.inter_ref and 'inter_ref' in col_map:
                    worksheet.write(row, col_map['inter_ref'], product.default_code or 'Not Available', text_format)  # type: ignore

                value = dict(
                    product._fields['type']._description_selection(product.env)  # type: ignore
                ).get(product.type)  # type: ignore
                worksheet.write(row, col_map['type'], value or 'Not Available', text_format)

                if self.print_category and 'category' in col_map:
                    worksheet.write(row, col_map['category'], product.categ_id.name or 'Not Available', text_format)  # type: ignore

                if self.print_uom and 'uom' in col_map:
                    worksheet.write(row, col_map['uom'], product.uom_id.name or 'Not Available', text_format)  # type: ignore

                if self.price and 'price' in col_map:
                    worksheet.write(row, col_map['price'], product.lst_price or 0.0, cell_format)  # type: ignore
        
                if self.description and 'description' in col_map:
                    html = product.description or ''

                    bold_format = workbook.add_format({
                        'bold': True,
                        'align': 'left',
                        'valign': 'vcenter',
                        'border': 1,
                        'text_wrap': True
                    })

                    normal_format = workbook.add_format({
                        'align': 'left',
                        'valign': 'vcenter',
                        'border': 1,
                        'text_wrap': True
                    })

                    soup = BeautifulSoup(html, "html.parser")
                    rich_text = []

                    for element in soup.descendants:
                        if element.name in ['strong', 'b']:
                            rich_text.append(bold_format)
                            rich_text.append(element.get_text())
                        elif element.name is None:
                            if element.parent.name not in ['strong', 'b']:
                                text = str(element).replace('\xa0', ' ')
                                if text.strip():
                                    rich_text.append(normal_format)
                                    rich_text.append(text)

                    if rich_text:
                        worksheet.write_rich_string(row, col_map['description'], *rich_text)
                    else:
                        description = html2plaintext(html).strip()
                        worksheet.write(row, col_map['description'], description or 'Not Found', text_format)
                    
                sr_no += 1
                row += 1

        workbook.close()
        excel_data = output.getvalue()
        output.close()

        attachment = self.env['ir.attachment'].create({
            'name': f'{self.catalog_name} Catalog Details',
            'type': 'binary',
            'raw': excel_data,
            'res_model': 'nf.generate.product.catalog.wizard',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        return attachment
        
    def download_xls_report(self):
        attachment = self.generate_xls_report()
        print("\n\n\n attachment",attachment)
        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content/{attachment.id}?download=true",
            'target': 'self',
        }

    def generate_pdf_attachment(self, report_xml_id, report_template_id, record_id=None, filename="Report.pdf"):
        if not record_id:
            record_id = self.id  # type: ignore

        report = self.env.ref(report_xml_id, raise_if_not_found=False)
        if not report:
            raise ValueError(f"Report XML ID not found: {report_xml_id}")
        
        pdf_report = self.env.ref(report_xml_id).sudo()._render_qweb_pdf(report_template_id,res_ids=[self.id])    #type: ignore
        pdf_content = pdf_report[0]
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'raw': pdf_content,
            'res_model': self._name,
            'res_id': record_id,
            'mimetype': 'application/pdf',
        })
        return attachment