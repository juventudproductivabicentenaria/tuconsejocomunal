# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class Partner(models.Model):
    _inherit = 'res.partner'
    
    is_council = fields.Boolean(
                    string='Es consejo', 
                    help="Indica sí el partner es un consejo comunal.",
                    )
    
    
class CommunalCouncil(models.Model):
	
    _name = "tcc.communal.council"
    _description = "Consejo Comunal"
    _inherits = {'res.users': 'user_id'}
    _rec_name = 'name'
    
    
    user_id = fields.Many2one(
                    'res.users', 
                    string='Usuario Consejo Comunal',
                    ondelete="cascade"
                    )
    situr_code = fields.Char(
                    string='Código SITUR',
                    )
    creation_date = fields.Date(
                    string='Fecha creación',
                    )
    rif = fields.Char(
                    string='RIF',
                    )
    state_id = fields.Many2one(
                    'res.country.state', 
                    string='Estado',
                    )
    #~ municipality_id = fields.Many2one(
                    #~ 'res.country.state.municipality', 
                    #~ string='Municipio',
                    #~ )
    #~ parish_id = fields.Many2one(
                    #~ 'res.country.state.municipality.parish', 
                    #~ string='Parroquia',
                    #~ )
    sector_id = fields.Many2one(
                'tcc.address.sector',
                string='Sector', 
                )
    active = fields.Boolean(default=True)
    
    
    _sql_constraints = [('situr_code_uniq', 'unique (situr_code)', "El Código SITUR ya Existe  !")]
    
    @api.onchange('creation_date')
    def to_validate_date(self):
        warning = {}
        result = {}
        if self.creation_date:
            if cmp(datetime.strptime(self.creation_date, DF).date(), date.today()) == 1:
                warning = {
                    'title': _('Warning!'),
                    'message': _('La fecha seleccionada no debe ser mayor a la fecha de hoy.'),
                }
                self.creation_date = False
                if warning:
                    result['warning'] = warning
            return result
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()
    
    @api.onchange('state_id')
    def onchangue_state(self):
        if self.state_id:
            self.municipality_id = False
            self.parish_id = False
            self.sector_id = False
    
    @api.onchange('municipality_id')
    def onchangue_municipality(self):
        if self.municipality_id:
            self.parish_id = False
            self.sector_id = False
            
    @api.multi
    def totalEdf(self):
		return self.env['tcc.dwelling.edifice'].search_count([('communal_council_id','=',self.id)])
		
    @api.multi
    def totalCas(self):
		return self.env['tcc.dwelling.house'].search_count([('communal_council_id','=',self.id)])
		
    @api.multi
    def totalFam(self):
		return self.env['tcc.family'].search_count([('communal_council_id','=',self.id)])
		
    @api.multi
    def totalDis(self):
		return self.env['tcc.distribution.delivery.confirmation'].search_count([('communal_council_id','=',self.id)])
    
    @api.model
    def create_default_survey(self):
        survey_model = self.env['survey.survey']
        survey_page_model = self.env['survey.page']
        survey_question_model = self.env['survey.question']
        survey_label_model = self.env['survey.label']
        
        survey_data = {
            'title': 'Participación Comunitaria',
            'auth_required': True,
            'tcc_survey': True,
            'communal_council_id': self.id,
        }
        survey = survey_model.create(survey_data)
        
        page_data = {
            'title': 'Participación Comunitaria',
            'description': 'Por favor, lea y responda las siguientes preguntas según sus observaciones respecto a su comunidad.',
            'survey_id': survey.id
            }
        survey_page = survey_page_model.create(page_data)
        quention_list = ['¿Conoce las Organizaciones Comunitarias que existen en su Comunidad?',
                        '¿Participa usted en algunas de ellas?',
                        '¿Participa algún miembro de su familia?',
                        '¿Cree Usted que en la actualidad el pueblo el pueblo está interviniendo en las decisiones sobre como deben gastarse los recursos de su comunidad?',
                        '¿Está de acuerdo que según la Constitución, es ahora el Pueblo organizado quien debe tener el protagonismo y el Poder para decidir de como invertir el presupuesto en su comunidad?',
                        '¿Tiene información sobre la propuesta de creación de Consejos Comunales?',
                        '¿Estaría dispuesto(a) a apoyar y participar en la creación de un Consejo Comunal en su comunidad?',
                        ]
        
        for sq in quention_list:
            question_data = {
                'question': sq,
                'constr_mandatory': True,
                'type': 'simple_choice',
                'page_id': survey_page.id
                }
            survey_question = survey_question_model.create(question_data)
        
            label_list = ['Si',
                          'No',
                         ]
            for sl in label_list:
                label_data = {
                    'question_id': survey_question.id,
                    'value': sl,
                    }
                survey_label = survey_label_model.create(label_data)
        question_data2 = {
                'question': '¿Cuáles misiones se están implementando en su comunidad?',
                'constr_mandatory': True,
                'type': 'multiple_choice',
                'page_id': survey_page.id
                }
        survey_question2 = survey_question_model.create(question_data2)
        label_list2 = ['Misión Ribas',
                       'Misión Sucre',
                       'Misión Vuelvan Caras',
                       'Misión Identidad',
                       'Misión Barrio Adentro',
                       'Misión Mercal',
                       'Misión Ezequiel Zamora',
                         ]
        for sl2 in label_list2:
            label_data2 = {
                'question_id': survey_question2.id,
                'value': sl2,
                }
            survey_label = survey_label_model.create(label_data2)
        return True
    
        
    @api.model
    def create(self, vals):
        council = super(CommunalCouncil, self).create(vals)
        list_group = []
        group_council = council.env['res.groups'].sudo().search([('name', '=', 'Consejo Comunal')])
        list_group.append(group_council.id)
        group_contact = council.env['res.groups'].sudo().search([('name', '=', 'Creación de contactos')])
        list_group.append(group_contact.id)
        group_employee = council.env['res.groups'].sudo().search([('name', '=', 'Empleado')])
        list_group.append(group_employee.id)
        council.sector_id.sudo().write({'communal_council_id': council.id})
        council.user_id.sudo().write({'is_council': True,'groups_id' : [(6,0,list_group)],'email' : council.user_id.login,'communal_council_id': council.id})
        users = council.env['res.users'].sudo().search([('id', '=', council.user_id.id)])
        #~ users = council.env['res.users'].sudo().search([('id', '=', council.user_id.id)])
        users.sudo().write({'communal_council_id': council.id})
        council.create_default_survey()
        return council
    
