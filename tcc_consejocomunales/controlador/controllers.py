# -*- coding: utf-8 -*-
from openerp import http

# class TccConsejocomunales(http.Controller):
#     @http.route('/tcc_consejocomunales/tcc_consejocomunales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tcc_consejocomunales/tcc_consejocomunales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tcc_consejocomunales.listing', {
#             'root': '/tcc_consejocomunales/tcc_consejocomunales',
#             'objects': http.request.env['tcc_consejocomunales.tcc_consejocomunales'].search([]),
#         })

#     @http.route('/tcc_consejocomunales/tcc_consejocomunales/objects/<model("tcc_consejocomunales.tcc_consejocomunales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tcc_consejocomunales.object', {
#             'object': obj
#         })