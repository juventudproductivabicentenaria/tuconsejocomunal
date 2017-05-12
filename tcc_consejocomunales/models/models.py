# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class partner(osv.osv):
    _name = 'res.partner'
    _inherit="res.partner"

    _columns = {
        'is_consejo': fields.boolean(
                    'Consejo Comunal'
                    ),
        
      'rif': fields.char(
                    'RIF',
                    default='J',
                    size=10,
                    required=True,
                    help='RIF del Consejo Comunal'
                    ),
     'estado_id':fields.many2one('res.estados','Estado',required=True),
     'municipio_id':fields.many2one('res.municipios','Municipio',required=True),
     'parroquia_id':fields.many2one('res.parroquias','Parroquia',required=True)
    }
    
    _defaults={
        'is_consejo':False
        }
        
    _sql_constraints = [
        ('rif_uniq', 'UNIQUE(rif)', 'El numero del rif debe ser único!'),
        ]
    
class tcc_consejocomunales(osv.osv):
     _name = 'tcc.consejocomunales'
     _inherits = {'res.partner': 'parent_id'}
     _rec_name='parent_id'
     
     _columns={
		'parent_id':fields.many2one(
                    'res.partner',
                    'Registro de los consejos Comunales',
                    required=True,
                    ondelete='cascade'
                    ),
        'cd_situr':fields.char('Codigo situr',size=13, help='Código Situr', required=True),
        'tlf':fields.char('Teléfono', size=11, help='Telefono', required=True),
        'fecha':fields.date('Fecha', size=20,help='Fecha de registro', required=True),
        'active':fields.boolean('Activo',help='Si esta activo el motor lo incluira en la vista...'),
        }
        
        
     def limpiar_campos(self,cr,uid,ids,nombre):
         res_users_obj = self.pool.get('res.users')
         res=res_users_obj.limpiar_campos(cr,uid,ids,nombre)
         return res
            
            
     _defaults={
        'active':True,
        'is_consejo':True
        }
        
     _sql_constraints = [
        ('cd_situr_uniq', 'UNIQUE(cd_situr)', 'El código Situr debe ser único!'),
        ('name_uniq', 'UNIQUE(parent_id)', 'El nombre del consejo comunal debe ser único!'),
        ('tlf_uniq', 'UNIQUE(tlf)', 'El número de teléfono debe ser único!'),
        ]
