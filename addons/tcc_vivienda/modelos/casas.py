# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class casas(osv.osv):
	_name = 'tcc.casas'
	_rec_name = 'nombre'

	_columns={
		'nombre': fields.char('Nombre de la Casa'),
		'numero': fields.integer('Numero de la Casa'),
		'viviendas_id': fields.many2one('tcc.viviendas', 'Vivienda'),
		'sector_id': fields.many2one('tcc.sectores', 'Sector'),
		'calleoavenida_id': fields.many2one('tcc.callesoavenidas','Calle o Avenida'),
		'active': fields.boolean('Activo', default=True),

	}