# -*- coding: utf-8 -*-

import odoo
from odoo import http
from odoo.http import request

from odoo.addons.web.controllers.main import Home


class Website(Home):

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        user_model = request.env['res.users'].sudo()
        notice = request.env['tcc.notice'].sudo()
        communal_model = request.env['tcc.communal.council'].sudo()
        user_data = user_model.browse(request.uid)
        communal_council_id = request.env['res.users'].sudo().browse(request.uid).communal_council_id.id
        if communal_council_id:
            notice_data = notice.search([('communal_council_id','=',communal_council_id)])
        else:
            notice_data = notice.search([])
        return request.render('tcc_communal_council.index',{
        'data_noticia':notice_data,
        })
