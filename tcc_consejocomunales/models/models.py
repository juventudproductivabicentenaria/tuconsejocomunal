# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class tcc_consejocomunales(osv.osv):
     _name = 'tcc.consejocomunales'
     _rec_name='nombre'
     
     _columns={
        'nombre':fields.char('Nombre del Consejo Comunal',size=200,required=True,help='Nombre del Consejo Comunal'),
        'rif':fields.char('Rif',size=10,required=True,help='Nombre del Consejo Comunal'),
        'cd_situr':fields.char('Código situr',size=20,required=True,help='Nombre del Consejo Comunal'),
        'active':fields.boolean('Activo',help='Si esta activo el motor lo incluira en la vista...')
        }
        
     _defaults={
        'active':True
        }
     
