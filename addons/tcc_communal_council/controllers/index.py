# -*- coding: utf-8 -*-

import odoo
from odoo import http
from odoo.http import request

from odoo.addons.web.controllers.main import Home


class Website(Home):

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        return request.render('tcc_communal_council.index',
                                        {})
