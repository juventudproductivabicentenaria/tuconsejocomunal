# -*- coding: utf-8 -*-

#MODELO QUE HEREDA A PADRE SURVEY.SURVEY

from openerp.osv import fields, osv

class survey_survey(osv.osv):
	_name = 'survey.survey'
	_inherit = 'survey.survey'

#SE AÑADE CAMPO PARA CONSEJOS COMUNALES AFECTANDO SURVEY_SURVEY
	_columns={
		'consejocomunal_id':fields.many2one(
                                'tcc.consejocomunales',
                                'Nombre del Consejo Comunal', 
                                required=True),
	}