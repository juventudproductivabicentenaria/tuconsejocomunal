# -*- coding: utf-8 -*-
from openerp import http

# class TccPersonas(http.Controller):
#     @http.route('/tcc_personas/tcc_personas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tcc_personas/tcc_personas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tcc_personas.listing', {
#             'root': '/tcc_personas/tcc_personas',
#             'objects': http.request.env['tcc_personas.tcc_personas'].search([]),
#         })

#     @http.route('/tcc_personas/tcc_personas/objects/<model("tcc_personas.tcc_personas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tcc_personas.object', {
#             'object': obj
#         })