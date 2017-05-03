# -*- coding: utf-8 -*-
from openerp import http

# class TccNoticias(http.Controller):
#     @http.route('/tcc_noticias/tcc_noticias/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tcc_noticias/tcc_noticias/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tcc_noticias.listing', {
#             'root': '/tcc_noticias/tcc_noticias',
#             'objects': http.request.env['tcc_noticias.tcc_noticias'].search([]),
#         })

#     @http.route('/tcc_noticias/tcc_noticias/objects/<model("tcc_noticias.tcc_noticias"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tcc_noticias.object', {
#             'object': obj
#         })