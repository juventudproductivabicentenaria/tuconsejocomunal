# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class tcc_familia(osv.osv):
     _name = 'tcc_familia.tcc_piso'
     _rec_name = 'piso'
     _columns = {
         'piso': fields.char('piso',required=True, help='Aquí se coloca el nombre o numero del piso '),
         'active': fields.boolean('activo'),
    
         }
     _defaults={
        'active':True,
         }

