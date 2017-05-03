# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class tcc_familia(osv.osv):
     _name = 'tcc_familia.tcc_apartamento'
     _rec_name = 'apartamento'
     _columns = {
         'apartamento': fields.char('apartamento',required=True, help='Aquí se coloca el nombre o numero del apartamento '),
         'active': fields.boolean('activo'),
  
         }
     _defaults={
        'active':True,
         }

