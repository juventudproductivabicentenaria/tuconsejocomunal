# -*- coding: utf-8 -*-

#~ from Excepciones import * #excepciones predefinidas
#~ import webkit             #logra hacer que el formato de la fecha sea igual a la conf regional.???
from datetime import * 


import calendar

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class partner(models.Model):
    _name = 'res.partner'
    _inherit="res.partner"

    is_persona = fields.Boolean(string='Persona', default=False)
    is_vocero = fields.Boolean(string='¿Es vocero?', default=False)
        

class TccPersons(models.Model):
    _name = "tcc.persons"
    _inherits = {'res.users': 'user_id'}
    _rec_name = 'name'
    _description = "Personas"
    
    
    user_id = fields.Many2one(
                'res.users', 
                string='Usuario Residente',
                ondelete="cascade"
                )
    cedula = fields.Char(
                string='Cédula',
                required = True,
                )
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                )
    family_id = fields.Many2one(
                'tcc.family',
                string='Familia', 
                )
    second_name = fields.Char(
                string='Segundo Nombre',
                required = True,
                )
    first_surname = fields.Char(
                string='Primer apellido',
                required = True,
                )
    second_surname = fields.Char(
                string='Segundo apellido',
                required = True,
                )
    birthdate = fields.Date(
                string='Fecha de nacimiento',
                index=True,
                )
    age = fields.Char(
                string='Edad',
                readonly=True,
                )
    civil_status = fields.Selection([
                ('Soltero','Soltero'),
                ('Casado','Casado'),
                ('Divorciado','Divorciado'),
                ('Viudo','Viudo'),],
                string='Estado civil',
                default='Soltero',
                required = True,
                )
    gender = fields.Selection([
                ('Masculino','Masculino'),
                ('Femenenino','Femenenino'),],
                string='Género',
                required = True,
                )
    nationality = fields.Selection([
                ('Venezolano','Venezolano'),
                ('Extrangero','Extrangero'),],
                string='Nacionalidad',
                required = True,
                )
    active = fields.Boolean(default=True)
    
    
    def es_bisiesto(self, y):
        'Devuelve un valor lógico indicando si el año pasado como argumento es bisiesto.'
        return y % 4 == 0 and y % 100 != 0 or y % 400 == 0

    def dias_mes(self, m, y):
        'Devuelve la cantidad de días que tiene un mes (m), según el año en que se encuentre (y).'
        if m == 2: return 29 if self.es_bisiesto(y) else 28
        return 30 if m in [4, 6, 9, 11] else 31

    def es_fecha(self,d, m, y):
        'Devuelve un valor lógico indicando si la fecha pasada como argumento es válida.'
        return not (d < 1 or d > self.dias_mes(m, y) or m < 1 or m > 12 or y < 1)

    def fin_mes(self, d, m, y):
        'Dada una fecha, devuelve los días que faltan para fin de mes.'
        dif = self.dias_mes(m, y) - d
        return dif

    def fin_anio(self, d, m, y):
        'Dada una fecha, devuelve los días que faltan para fin de año.'
        dif = 365 - self.dias_transcurridos(d, m, y)
        if self.es_bisiesto(y): dif += 1
        return dif

    def dias_transcurridos(self, d, m, y):
        'Devuelve los días transcurridos desde principio de año hasta el día de la fecha pasada como argumento.'
        dias = 0
        for i in range(1, m): dias += self.dias_mes(i, y)
        dias += d
        return dias
    
    @api.onchange('birthdate')
    def to_calculate_age(self):
        #~ datetime.now().date() - datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()).days
        warning = {}
        result = {}
        if self.birthdate:
            if cmp(datetime.strptime(self.birthdate, DF).date(), date.today()) == 1:
                warning = {
                    'title': _('Warning!'),
                    'message': _('La fecha seleccionada no debe ser mayor a la fecha de hoy.'),
                }
                self.birthdate = False
                if warning:
                    result['warning'] = warning
                return result
            else:
                y1,m1,d1 = self.birthdate.split('-')
                y2 = date.today().year
                m2 = date.today().month
                d2 = date.today().day
                yf, mp = 0, 0
                for h in range(int(m1) + 1, 13):
                    mp += 1
                for i in range(1, y2 - int(y1)):
                    yf += 1
                    for j in range(1, 13):
                        mp += 1
                for k in range(1, m2):
                    mp += 1
                    
                mf = mp % 12
                df = self.fin_mes(int(d1), int(m1), int(y1)) + d2 - 1
                if df > self.dias_mes(int(m1), int(y1)):
                    df -= self.dias_mes(int(m1), int(m1)) - 1
                    mf += 1
                
                ys = '' if yf == 1 else 's'
                ms = '' if mf == 1 else 'es'
                ds = '' if df == 1 else 's'
                #~ if yf == 0:
                    #~ self.age = '%d mes%s y %d día%s.' % (mf, ms, df, ds)
                print 'La diferencia entre ambas fechas es de %d año%s, %d mes%s y %d día%s.' % (yf, ys, mf, ms, df, ds)
                print 'La diferencia entre ambas fechas es de %d año%s, %d mes%s y %d día%s.' % (yf, ys, mf, ms, df, ds)
                print 'La diferencia entre ambas fechas es de %d año%s, %d mes%s y %d día%s.' % (yf, ys, mf, ms, df, ds)
                print 'La diferencia entre ambas fechas es de %d año%s, %d mes%s y %d día%s.' % (yf, ys, mf, ms, df, ds)
                print 'La diferencia entre ambas fechas es de %d año%s, %d mes%s y %d día%s.' % (yf, ys, mf, ms, df, ds)
                print 'La diferencia entre ambas fechas es de %d año%s, %d mes%s y %d día%s.' % (yf, ys, mf, ms, df, ds)
                print 'La diferencia entre ambas fechas es de %d año%s, %d mes%s y %d día%s.' % (yf, ys, mf, ms, df, ds)
                
                
            return result
        
        
        
        
        
        
