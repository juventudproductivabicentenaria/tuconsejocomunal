# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class viviendas(osv.osv):
	_name = 'tcc.viviendas'

	_columns={
		'consejocomunal_id': fields.many2one('tcc.consejocomunales','Nombre del Consejo Comunal', required=True),
		'casas_ids': fields.one2many('tcc.casas','viviendas_id','Casas'),
		'edificios_ids': fields.one2many('tcc.edificios','viviendas_id','Edificios'),
		'active': fields.boolean('Activo', default=True),
	}
