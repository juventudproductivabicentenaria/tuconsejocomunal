# -*- coding: utf-8 -*-

import odoo
from odoo import http
from odoo.http import request

from odoo.addons.web.controllers.main import Home


class Website(Home):

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        
        return request.render('tcc_communal_council.index5',
                                        {'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"]})
                                        
                                        
    @http.route('/menudata', type='json', auth="public", website=True)
    def menudata(self):
        res={'menus':[],'componente':''}
        Menu = request.env['website.menu']
        menu_data=Menu.search_read(fields=['name','new_window','url'],domain=[('parent_id','=',1)])
        print menu_data
        print menu_data
        print menu_data
        return menu_data
                                        
   
