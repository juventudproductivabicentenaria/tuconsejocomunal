# -*- coding: utf-8 -*-

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
                age_now = (date.today() - datetime.strptime(self.birthdate, DF).date()).days / 365
                print age_now
                print age_now
                print age_now
                print age_now
                self.age = age_now
            return result
    
    #~ def _onchange_uom_id(self):
        #~ warning = {}
        #~ result = {}
        #~ if not self.uom_id:
            #~ self.price_unit = 0.0
        #~ if self.product_id and self.uom_id:
            #~ if self.product_id.uom_id.category_id.id != self.uom_id.category_id.id:
                #~ warning = {
                    #~ 'title': _('Warning!'),
                    #~ 'message': _('The selected unit of measure is not compatible with the unit of measure of the product.'),
                #~ }
                #~ self.uom_id = self.product_id.uom_id.id
        #~ if warning:
            #~ result['warning'] = warning
        #~ return result
    
