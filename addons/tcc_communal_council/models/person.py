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
                required = False,
                )
    first_surname = fields.Char(
                string='Primer apellido',
                required = True,
                )
    second_surname = fields.Char(
                string='Segundo apellido',
                required = False,
                )
    birthdate = fields.Date(
                string='Fecha de nacimiento',
                index=True,
                )
    entry_count = fields.Integer(compute='_entry_count', string='# Asset Entries')
    age = fields.Char(
                compute='_to_calculate_age',
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
    
    _sql_constraints = [('cedula_uniq', 'unique (cedula)', "La Cédula ya Existe, Verifique!")]
    
    @api.onchange('birthdate')
    def to_validate_date(self):
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
        
    
    @api.multi
    @api.depends('birthdate')
    def _to_calculate_age(self):
        if self.birthdate:
            date_ncmto = datetime.strptime(self.birthdate, '%Y-%m-%d')
            month_days = calendar.monthrange(date_ncmto.year, date_ncmto.month)[1]
            days = month_days - date_ncmto.day + 1
            age_year = (date.today() - datetime.strptime(self.birthdate, DF).date()).days / 365
            remaining_days = (date.today() - datetime.strptime(self.birthdate, DF).date()).days % 365
            age_month = remaining_days / month_days
            age_days = remaining_days % month_days
            
            ys = '' if age_year == 1 else 's'
            ms = '' if age_month == 1 else 'es'
            ds = '' if age_days == 1 else 's'
            if age_year > 0 and age_month > 0 and age_days > 0:
                self.age = '%d año%s, %d mes%s y %d día%s.' % (age_year, ys, age_month, ms, age_days, ds)
            elif age_year <= 0 and age_month > 0 and age_days > 0:
                self.age = '%d mes%s y %d día%s.' % (age_month, ms, age_days, ds)
            elif age_year > 0 and age_month <= 0 and age_days > 0:
                self.age = '%d año%s y %d día%s.' % (age_year, ys, age_days, ds)
            elif age_year > 0 and age_month > 0 and age_days <= 0:
                self.age = '%d año%s y %d mes%s.' % (age_year, ys, age_month, ms)
            elif age_year <= 0 and age_month <= 0 and age_days > 0:
                self.age = '%d día%s.' % (age_days, ds)
            elif age_year <= 0 and age_month > 0 and age_days <= 0:
                self.age = '%d mes%s.' % (age_month, ms)
            elif age_year > 0 and age_month <= 0 and age_days <= 0:
                self.age = '%d año%s.' % (age_year, ys)
