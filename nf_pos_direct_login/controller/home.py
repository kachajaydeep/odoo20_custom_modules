# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import http   #type: ignore
from odoo.http import request   #type: ignore
from odoo.addons.web.controllers.home import Home
from odoo.addons.point_of_sale.controllers.main import PosController

class HomeInherit(Home):
    
    @http.route()
    def web_client(self, s_action=None, **kw):
        if request.session.uid:
            user = request.env["res.users"].sudo().browse(request.session.uid)
            if(user.has_group('point_of_sale.group_pos_user')):
                if user.pos_only_user and user.default_pos_config_id and user.default_pos_config_id.nf_enable_direct_login:
                    return request.redirect(
                        f"/pos/ui?config_id={user.default_pos_config_id.id}"
                    )

        return super().web_client(s_action=s_action, **kw)
    
    @http.route()
    def web_login(self, redirect=None, **kw):
        response = super().web_login(redirect=redirect, **kw)

        if(request.session.uid and request.httprequest.method == 'POST'):
            user = request.env["res.users"].sudo().browse(request.session.uid)
            
            if not user.has_group('point_of_sale.group_pos_user'):
                request.params['login_success'] = False

                return request.redirect(
                    "/web/login?error=pos_access_error"
                )
                
            if user.pos_only_user and user.default_pos_config_id and user.default_pos_config_id.nf_enable_direct_login:
                return request.redirect(
                    f"/pos/ui?config_id={user.default_pos_config_id.id}"
                )
        return response
    
class PosConteollerInherit(PosController):
    
    @http.route()
    def pos_web(self, config_id=False, from_backend=False, subpath=None, **k):
        if request.session.uid:
            user = request.env["res.users"].sudo().browse(request.session.uid)
            if user.pos_only_user and user.default_pos_config_id and user.default_pos_config_id.nf_enable_direct_login:
                default_config_id = user.default_pos_config_id.id
                requested_config_id = False
                if config_id:
                    try:
                        requested_config_id = int(config_id)
                    except (TypeError, ValueError):
                        requested_config_id = False

                if requested_config_id != default_config_id:
                    return request.redirect(
                        f"/pos/ui?config_id={default_config_id}"
                    )

        return super().pos_web(config_id=config_id, from_backend=from_backend, subpath=subpath, **k)