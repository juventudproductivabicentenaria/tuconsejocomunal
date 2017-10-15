# -*- coding: utf-8 -*-
import logging
import werkzeug

from openerp import http
from openerp.http import request
from openerp.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError

class CommunalAuthSignupHome(AuthSignupHome):


    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        state_model=request.env["res.country.state"]
        country_model=request.env["res.country"]
        qcontext = self.get_auth_signup_qcontext()
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                return super(AuthSignupHome, self).web_login(*args, **kw)
            except (SignupError, AssertionError), e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error(e.message)
                    qcontext['error'] = _("Could not create a new account.")
        country_id=country_model.search([('code','=','VE')])
        state_data=state_model.name_search(args=[('country_id','=',country_id.id)])
        qcontext.update({'state_data':state_data}) 
        return request.render('auth_signup.signup', qcontext)

    @http.route('/web/signup/municipality', type='json', auth='public', website=True)
    def web_municipality_data(self, **kw):
        municipality_model=request.env["res.country.state.municipality"]
        municipality_data=municipality_model.name_search(args=[('state_id','=',int(kw['state_id']))])
        print municipality_data
        return {'data':municipality_data}
        
        
