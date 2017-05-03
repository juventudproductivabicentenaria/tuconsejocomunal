# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class tcc_familia(osv.osv):
     _name = 'tcc_familia.tcc_familia'
     _rec_name = 'nombre'
     
     tenencia_data=[
                ('propia', 'propia'),
                ('alquilada', 'alquilada'),
                ('invadida','invadida'),
                ('adjudicada','adjudicada')
                ]
                
     tipo_vivienda_data=[
                ('casa', 'Casa'),
                ('edificio', 'Edificio')
                ]
                
     _columns = {
         
         
         'nombre':fields.char(
                            'Nombre de la Familia', 
                            required=True,
                            help='Aquí se coloca el nombre de la familia'),
         'vivienda':fields.selection(
                            tipo_vivienda_data, 
                            'Tipo de Vivienda',
                            required=True,),
         'apartamento_id':fields.many2one(
                                'tcc_familia.tcc_apartamento',
                                'Apartamento',),
         'piso_id':fields.many2one(
                            'tcc_familia.tcc_piso',
                            'Piso'),
         'consejocomunal_id':fields.many2one(
                                'tcc.consejocomunales',
                                'Nombre del Consejo Comunal', 
                                required=True),
         'casa_id':fields.many2one(
                        'tcc.casas',
                        'Casa'),
         'edificio_id':fields.many2one(
                        'tcc.edificios',
                        'Edificio'),
         'fecha_antiguedad':fields.date(
                        'Fecha de Antiguedad',
                        help="""Aquí se coloca la fecha de antiguedad 
                               de la Familia en la comunidad"""),
         'tenencia':fields.selection(
                        tenencia_data, 
                        'Tenencia de la Vivienda',
                        required=True,),
         'active':fields.boolean('Activo'),
        
         }
    
     _defaults={
        'active':True,
         }
    

