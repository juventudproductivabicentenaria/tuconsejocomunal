# -*- coding: utf-8 -*-


from openerp.osv import fields, osv

class project(osv.osv):
     _name = 'project.project'
     _inherit=['project.project']
     
     _columns={
		'consejocomunal_id':fields.many2one('tcc.consejocomunales','Nombre del Consejo Comunal', required=True),
	}
