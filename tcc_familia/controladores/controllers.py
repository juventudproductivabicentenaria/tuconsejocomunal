# -*- coding: utf-8 -*-
from openerp import http

# class TccFamilia(http.Controller):
#     @http.route('/tcc_familia/tcc_familia/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tcc_familia/tcc_familia/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tcc_familia.listing', {
#             'root': '/tcc_familia/tcc_familia',
#             'objects': http.request.env['tcc_familia.tcc_familia'].search([]),
#         })

#     @http.route('/tcc_familia/tcc_familia/objects/<model("tcc_familia.tcc_familia"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tcc_familia.object', {
#             'object': obj
#         })