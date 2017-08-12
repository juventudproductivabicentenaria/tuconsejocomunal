# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
import re
import uuid
import urlparse

from odoo import api, fields, models, _
from odoo.exceptions import UserError

emails_split = re.compile(r"[;,\n\r]+")
email_validator = re.compile(r"[^@]+@[^@]+\.[^@]+")

class TccSurvey(models.Model):
    _inherit = 'survey.survey'
    
    @api.multi
    def default_communal_council(self):
        list_group_name = []
        for name_goup in self.env.user.groups_id:
            list_group_name.append(name_goup.name)
        if 'Consejo Comunal' in list_group_name:
            return self.env['tcc.communal.council'].search([('user_id', '=', self.env.uid)]).id
        if 'Vocero' in list_group_name:
            return self.env['tcc.communal.council'].search([('communal_council_id.user_id', '=', self.env.user.communal_council_id.user_id.id)]).id
        if 'Residente del Consejo Comunal' in list_group_name:
            return self.env['tcc.communal.council'].search([('communal_council_id.user_id', '=', self.env.uid)]).id
            
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                default = default_communal_council,
                readonly = True,
                )
    tcc_survey = fields.Boolean('Default Survey', default = False)
    
    



class TccSurveyMailComposeMessage(models.TransientModel):
    _inherit = 'survey.mail.compose.message'
    _description = 'Domain for Partner'
    
    
    @api.onchange('partner_ids')
    def domain_partner(self):
        list_partner = []
        Users = self.env['res.users'].search([('communal_council_id', '=', self.survey_id.communal_council_id.id)])
        for parner in Users:
            list_partner.append(parner.partner_id.id)
        domain = {'partner_ids': [('id', 'in', list_partner)]}
        return {'domain': domain}
