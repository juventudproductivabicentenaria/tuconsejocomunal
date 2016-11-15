# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class edificios(osv.osv):
	_name = 'tcc.edificios'
	_rec_name = 'nombre'

	_columns={
		'nombre': fields.char('Nombre del Edificio'),
		'viviendas_id': fields.many2one('tcc.viviendas','Vivienda'),
		'sector_id': fields.many2one('tcc.sectores', 'Sector'),
		'calleoavenida_id': fields.many2one('tcc.callesoavenidas','Calle o Avenida'),
		'active': fields.boolean('Activo', default=True),

	}