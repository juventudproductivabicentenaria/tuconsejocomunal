# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class tcc_categorias(osv.osv):
     _name = 'tcc_categorias.tcc_categorias'
     _rec_name = 'categorias'

     
     _columns={
        'categorias':fields.char('categorias',size=50,required=True,help='categorias'),
        'active':fields.boolean('Activar',help='Si esta activo el motor lo incluira en la vista...'),
        }
        
     _defaults={
        'active':True,
        }
