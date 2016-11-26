# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class tcc_encuesta(osv.osv):
	_name = 'tcc_encuesta'
	_inherit = 'survey.survey'

	_columns={
		'crear_encuesta':fields.many2one('survey.survey','Crear Encuesta'),
		'editar_encuesta':fields.many2one('survey.survey',''),
		'enviar_encuesta':fields.many2one('survey.survey',''),
		'consejocomunal_id':fields.many2one(
                                'tcc.consejocomunales',
                                'Nombre del Consejo Comunal', 
                                required=True),
	}
