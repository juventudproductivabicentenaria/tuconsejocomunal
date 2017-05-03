# -*- coding: utf-8 -*-
from openerp import http

# class TccViviendas(http.Controller):
#     @http.route('/tcc_viviendas/tcc_viviendas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tcc_viviendas/tcc_viviendas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tcc_viviendas.listing', {
#             'root': '/tcc_viviendas/tcc_viviendas',
#             'objects': http.request.env['tcc_viviendas.tcc_viviendas'].search([]),
#         })

#     @http.route('/tcc_viviendas/tcc_viviendas/objects/<model("tcc_viviendas.tcc_viviendas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tcc_viviendas.object', {
#             'object': obj
#         })
