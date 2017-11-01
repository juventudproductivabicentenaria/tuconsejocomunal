# -*- coding: utf-8 -*-
import odoo
from odoo import http
from odoo.http import request

from odoo.addons.web.controllers.main import Home

class Index(http.Controller):
    @http.route('/register/communalcouncil/', auth='public', website=True, type="http")
    def index(self, **kw):
    	countries = http.request.env['res.country'].sudo().search([])
    	states = http.request.env['res.country.state'].sudo().search([])
    	municipalities = http.request.env['res.country.state.municipality'].sudo().search([])
    	parishes = http.request.env['res.country.state.municipality.parish'].sudo().search([])
        return request.render('tcc_communal_council.index',
        	{'states': states,'municipalities': municipalities, 'parishes': parishes, 'countries': countries

        	}
        	)