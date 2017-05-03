# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class callesoavenidas(osv.osv):
	_name = 'tcc.callesoavenidas'
	_rec_name = 'nombre'

	_columns={
		'nombre': fields.char('Nombre de la calle o avenida'),
		'active': fields.boolean('Activo', default=True),
	}