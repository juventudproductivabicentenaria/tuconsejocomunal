# -*- coding: utf-8 -*-
from odoo import http

class SvgEjemplo(http.Controller):
    
     @http.route('/svg', type='http', auth="public", website=True)
     def list(self, **kw):
         return http.request.render('svg_ejemplo.listing2', {})

     
