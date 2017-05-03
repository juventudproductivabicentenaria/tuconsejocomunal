# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class sectores(osv.osv):
	_name = 'tcc.sectores'
	_rec_name = 'nombre'

	_columns={
		'nombre': fields.char('Nombre del Sector'),
		'active': fields.boolean('Activo', default=True),
	}