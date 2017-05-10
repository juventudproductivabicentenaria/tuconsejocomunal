# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date

from openerp.osv import fields, osv
from openerp.exceptions import UserError
from openerp import api

class partner(osv.osv):
    _name = 'res.partner'
    _inherit="res.partner"

    _columns = {
        'is_consejo': fields.boolean(
                    'Consejo Comunal',
                    required=True,
                    ),

        'rif': fields.char(
                    'RIF',
                    size=15,
                    required=True,
                    help='Número del R.I.F. de la Entidad'
                    ),
        'estado_id':fields.many2one(
                    'res.estados',
                    'Estado',
                    required=True,
                    ),
        'municipio_id':fields.many2one(
                    'res.municipios',
                    'Municipio',
                    required=True,
                    ),
        'parroquia_id':fields.many2one(
                    'res.parroquias',
                    'Parroquia',
                    required=True
                    ),
        'ubicacion': fields.char(
                    'Ubicación',
                    required=True,
                    help='Dirección específica'
                    ),
    }
    
    _defaults={
        'is_consejo':False
        }
        
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'name':vals['name'].upper(),
            'ubicacion':vals['ubicacion'].upper(),
            })
        return super(partner, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if 'name' in vals.keys():
            vals.update({'name':vals['name'].upper(),})
        if 'ubicacion' in vals.keys():
            vals.update({'ubicacion':vals['ubicacion'].upper(),})
        return super(partner, self).write(cr, uid, ids, vals, context=context)

class tcc_consejocomunales(osv.osv):
    _name = 'tcc.consejocomunales'
    _inherits = {'res.partner': 'parent_id'}
    _rec_name='parent_id'

    _columns={
        'parent_id':fields.many2one(
                    'res.partner',
                    'Registro de los consejos Comunales',
                    #~ required=True,
                    ondelete='cascade',
                    ),
        'cd_situr':fields.char(
                    'Código SITUR',
                    help='Nombre del Consejo Comunal',
                    ),
        'fecha':fields.date(
                    'Fecha de creación',
                    help='Nombre del Consejo Comunal',
                    ),
        'active':fields.boolean('Activo',
                    help='Si esta activo el motor lo incluiraá en la vista...'),
    }


    def limpiar_campos(self,cr,uid,ids,nombre):
        res_users_obj = self.pool.get('res.users')
        res=res_users_obj.limpiar_campos(cr,uid,ids,nombre)
        return res


    _defaults={
        'active':True,
        'is_consejo':True
    }
    
    def on_change_validate_date(self, cr, uid, ids, fecha, context=None):
        res = {}
        msg = {}
        if fecha:
            if cmp(datetime.strptime(fecha, '%Y-%m-%d').date(), date.today()) == 1:
                msg = {
                    'title':('Error de fecha'),
                    'message':('La fecha seleccionada no puede ser mayor a la fecha de hoy.'),
                        }
                res = {
                    'fecha':'',
                    }
        return {'warning':msg, 'value':res}
    
    
