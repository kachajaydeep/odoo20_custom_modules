# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import http
from odoo.http import request
import requests
from urllib.parse import quote_plus

class NfCustomFontController(http.Controller):

    @http.route('/nf_custom_font_family/dynamic_css',type='http',auth='user',cors='*')
    def get_custom_font(self):
        is_custom_font = request.env['ir.config_parameter'].sudo().get_bool('nf_custom_font_family.nf_is_custom_font')

        if is_custom_font:
            try:
                nf_ICP_sudo = request.env['ir.config_parameter'].sudo()
                user_font_choise = nf_ICP_sudo.get_str('nf_custom_font_family.nf_font_family')
                font_map = {
                    'montserrat':"'Montserrat', sans-serif",
                    'open_Sans':"'Open Sans',sans-serif",
                    'raleway':"'Raleway',sans-serif",
                    'oswald':"'Oswald',cursive",
                }

                google_import_url = ""

                if user_font_choise != 'custom':
                    user_selected_fonts = font_map.get(user_font_choise ,"'Montserrat', sans-serif")
                    
                else:            
                    custom_name = nf_ICP_sudo.get_str('nf_custom_font_family.nf_text', 'Poppins')
                    if ',' in custom_name:
                        user_selected_fonts = custom_name
                        url_formate = custom_name.split(',')[0].strip().replace("'", "").replace('"', '').replace(' ', '+')
                        google_import_url = f"@import url('https://fonts.googleapis.com/css2?family={url_formate}:wght@300;400;500;700&display=swap');"
                    else:
                        custom_name = custom_name.strip().strip("'\"")
                        url_formate = quote_plus(custom_name)
                        google_import_url = f"@import url('https://fonts.googleapis.com/css2?family={url_formate}:wght@300;400;500;700&display=swap');"
                        user_selected_fonts = f"'{custom_name}', sans-serif"

                css_content = f"""
                    {google_import_url}

                    :root, body, .o_web_client,.o_base_settings_view,.app_settings_block,h1,.h1,h2,.h2,h3,.h3,h4,.h4,h5,.h5,h6,.h6 ,.o_main_navbar, .modal, .popover, .tooltip {{
                            font-family: {user_selected_fonts} !important;
                        }}
                    """
                return request.make_response(css_content, [('Content-Type', 'text/css')])
                
            except Exception as e:
                fallback_css = ":root, body, .o_web_client { font-family: 'Montserrat', sans-serif !important; }"
                return request.make_response(fallback_css, [('Content-Type', 'text/css')])