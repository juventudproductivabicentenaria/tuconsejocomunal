# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import werkzeug
from datetime import datetime
from math import ceil

from odoo import fields, http, SUPERUSER_ID
from odoo.http import request
from odoo.tools import ustr

from odoo.addons.survey.controllers.main import WebsiteSurvey



_logger = logging.getLogger(__name__)


class WebsiteSurvey(WebsiteSurvey):
    # HELPER METHODS #

    
    # Survey start
    @http.route(['/survey/start/<model("survey.survey"):survey>',
                 '/survey/start/<model("survey.survey"):survey>/<string:token>'],
                type='http', auth='public', website=True)
    def start_survey(self, survey, token=None, **post):
        UserInput = request.env['survey.user_input']
        print type(token)
        # Test mode
        if token and token == "phantom":
            _logger.info("[survey] Phantom mode")
            user_input = UserInput.create({'survey_id': survey.id, 'test_entry': True})
            data = {'survey': survey, 'page': None, 'token': user_input.token}
            return request.render('survey.survey_init', data)
        
        if 'tcc' in token.split('-'):
            ts = token.split('-')
            vals = {'survey_id': survey.id}
            vals['partner_id'] = int(ts[0])
            user_input = UserInput.create(vals)
            data = {'survey': survey, 'page': None, 'token': user_input.token}
            return request.render('survey.survey_init', data)

        # Controls if the survey can be displayed
        errpage = self._check_bad_cases(survey, token=token)
        if errpage:
            return errpage

        # Manual surveying
        elif not token:
            vals = {'survey_id': survey.id}
            if request.website.user_id != request.env.user:
                vals['partner_id'] = request.env.user.partner_id.id
            user_input = UserInput.create(vals)
        else:
            user_input = UserInput.sudo().search([('token', '=', token)], limit=1)
            if not user_input:
                return request.render("website.403")

        # Do not open expired survey
        errpage = self._check_deadline(user_input)
        if errpage:
            return errpage

        # Select the right page
        if user_input.state == 'new':  # Intro page
            data = {'survey': survey, 'page': None, 'token': user_input.token}
            return request.render('survey.survey_init', data)
        else:
            return request.redirect('/survey/fill/%s/%s' % (survey.id, user_input.token))

    
