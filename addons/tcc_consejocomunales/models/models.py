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
                    size=15,
                    required=True,
                    help='Número del R.I.F. de la Entidad'
                    ),
     'estado_id':fields.many2one('res.estados','Estado',required=True),
     'municipio_id':fields.many2one('res.municipios','Municipio',required=True),
     'parroquia_id':fields.many2one('res.parroquias','Parroquia',required=True)
    }
    
    _defaults={
        'is_consejo':False
        }

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
        'cd_situr':fields.char('Código situr',help='Nombre del Consejo Comunal'),
        'fecha':fields.date('Fecha',size=20,help='Nombre del Consejo Comunal'),
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
     
