# -*- coding: utf-8 -*-
from openerp import http

# class TccGentionconsejos(http.Controller):
#     @http.route('/tcc_gentionconsejos/tcc_gentionconsejos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tcc_gentionconsejos/tcc_gentionconsejos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tcc_gentionconsejos.listing', {
#             'root': '/tcc_gentionconsejos/tcc_gentionconsejos',
#             'objects': http.request.env['tcc_gentionconsejos.tcc_gentionconsejos'].search([]),
#         })

#     @http.route('/tcc_gentionconsejos/tcc_gentionconsejos/objects/<model("tcc_gentionconsejos.tcc_gentionconsejos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tcc_gentionconsejos.object', {
#             'object': obj
#         })