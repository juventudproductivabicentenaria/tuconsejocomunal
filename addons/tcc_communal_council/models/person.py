# -*- coding: utf-8 -*-

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
        
class Users(models.Model):
    _name = 'res.users'
    _inherit="res.users"

    
    @api.multi
    def default_communal_council(self):
        list_group_name = []
        for name_goup in self.env.user.groups_id:
            list_group_name.append(name_goup.name)
        if 'Consejo Comunal' in list_group_name:
            return self.env['tcc.communal.council'].search([('user_id', '=', self.env.uid)]).id
        if 'Vocero' or 'Residente del Consejo Comunal' in list_group_name:
            return self.env['tcc.communal.council'].search([('communal_council_id.user_id', '=', self.env.user.communal_council_id.user_id.id)]).id
        if 'Residente del Consejo Comunal' in list_group_name:
            return self.env['tcc.communal.council'].search([('communal_council_id.user_id', '=', self.env.uid)]).id
    
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                default=default_communal_council,
                readonly=True,
                )
    
    
class TccPersons(models.Model):
    _name = "tcc.persons"
    _inherits = {'res.users': 'user_id'}
    _rec_name = 'name'
    _description = "Personas"
    
    
    @api.depends('birthdate')
    def to_calculate_age(self):
        for line in self:
            if line.birthdate:
                date_ncmto = datetime.strptime(line.birthdate, '%Y-%m-%d')
                month_days = calendar.monthrange(date_ncmto.year, date_ncmto.month)[1]
                days = month_days - date_ncmto.day + 1
                age_year = (date.today() - datetime.strptime(line.birthdate, DF).date()).days / 365
                if age_year >= 15:
                    line.fifteen = True
                else:
                    line.fifteen = False
                remaining_days = (date.today() - datetime.strptime(line.birthdate, DF).date()).days % 365
                age_month = remaining_days / month_days
                age_days = remaining_days % month_days
                
                ys = '' if age_year == 1 else 's'
                ms = '' if age_month == 1 else 'es'
                ds = '' if age_days == 1 else 's'
                if age_year > 0 and age_month > 0 and age_days > 0:
                    line.age = '%d año%s, %d mes%s y %d día%s.' % (age_year, ys, age_month, ms, age_days, ds)
                elif age_year <= 0 and age_month > 0 and age_days > 0:
                    line.age = '%d mes%s y %d día%s.' % (age_month, ms, age_days, ds)
                elif age_year > 0 and age_month <= 0 and age_days > 0:
                    line.age = '%d año%s y %d día%s.' % (age_year, ys, age_days, ds)
                elif age_year > 0 and age_month > 0 and age_days <= 0:
                    line.age = '%d año%s y %d mes%s.' % (age_year, ys, age_month, ms)
                elif age_year <= 0 and age_month <= 0 and age_days > 0:
                    line.age = '%d día%s.' % (age_days, ds)
                elif age_year <= 0 and age_month > 0 and age_days <= 0:
                    line.age = '%d mes%s.' % (age_month, ms)
                elif age_year > 0 and age_month <= 0 and age_days <= 0:
                    line.age = '%d año%s.' % (age_year, ys)
    
    
    
    workplace_data=[
                ('public_institution', 'Institución pública'),
                ('private_institution', 'Institución privada'),
                ('commercial', 'Comercial'),
                ('own_account', 'Cuenta propia'),
                ('peddling', 'Buhonería'),
                ('other', 'Otro'),
                ]
    user_id = fields.Many2one(
                'res.users', 
                string='Persona',
                required = False,
                #~ ondelete="cascade"
                )
    family_id = fields.Many2one(
                'tcc.family', 
                string='Usuario Residente',
                #~ ondelete="cascade",
                required = False,
                )
    cedula = fields.Char(
                string='Cédula',
                required = False,
                )
    first_name = fields.Char(
                string='Primer Nombre',
                required = True,
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
    kinship_id = fields.Many2one(
                'tcc.persons.kinship', 
                string='Parentesco',
                #~ ondelete="cascade",
                required = False,
                help="Relación de afinidad con el Jefe de la familia."
                )
    birthdate = fields.Date(
                string='Fecha de nacimiento',
                required=True,
                )
    age = fields.Char(
                compute='to_calculate_age',
                string='Edad',
                readonly=True,
                #~ store=True,
                )
    civil_status = fields.Selection([
                ('Soltero','Soltero(a)'),
                ('Casado','Casado(a)'),
                ('Divorciado','Divorciado(a)'),
                ('Comcubino','Comcubino(a)'),
                ('Viudo','Viudo(a)'),],
                string='Estado civil',
                default='Soltero',
                required = True,
                )
    level_instruccion = fields.Selection([
                ('sin_instruccion','Sin Instrucción'),
                ('Basica','Básica'),
                ('Bachiller','Bachiller'),
                ('tecnico_medio','Técnico Medio'),
                ('tecnico_superior','Técnico Superior'),
                ('Universitario','Universitario'),
                ('post_grado','Post Grado'),],
                string='Nivel de instrucción',
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
                ('Extranjero','Extranjero'),],
                string='Nacionalidad',
                required = True,
                )
    have_work = fields.Selection([
                ('Si','Si'),
                ('No','No'),],
                string='Posee trabajo',
                required = True,
                )
    type_family_income = fields.Selection([
                ('Diario','Diario'),
                ('Semanal','Semanal'),
                ('Quincenal','Quincenal'),
                ('Mensual','Mensual'),
                ('trabajo_realizado','Por Trabajo Realizado'),],
                string='Tipo ingreso familiar',
                )
    profession_id = fields.Many2one(
                'tcc.persons.profession',
                string='Profesión/Oficio',
                required = False,
                help="Indique a que se dedica.",
                )
    monthly_income = fields.Float(
                string='Ingreso Mensual',
                required=False,
                )
    is_family_boss = fields.Boolean(
                string='Jefe de familia',
                )
    fifteen = fields.Boolean(string='Mayor de quince años', default=False)
    registered_cne = fields.Selection([
                ('Si','Si'),
                ('No','No'),],
                string='Registrado en CNE',
                required = True,
                )
    into_committee = fields.Boolean(
                'Pertenece a un comite',
                default=False
                )
    bank_account = fields.Selection(
                [('Si', 'Si'),
                ('No', 'No'),],
                string='Tiene cuenta bancaria', 
                )
    credit_card = fields.Selection(
                [('Si', 'Si'),
                ('No', 'No'),],
                string='Tiene tarjeta de crédito', 
                )
    cesta_ticket = fields.Selection(
                [('Si', 'Si'),
                ('No', 'No'),],
                string='Tiene cesta ticket', 
                )
    workplace = fields.Selection(
                workplace_data, 
                string='Lugar de trabajo', 
                )
    name_workplace = fields.Char(
                string='Nombre del lugar de trabajo',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('cedula_uniq', 'unique (cedula)', "La Cédula ya Existe, Verifique!")]
    
    @api.onchange('workplace')
    def no_workplace(self):
        if self.workplace != 'other':
            self.name_workplace = False
    
        
    @api.onchange('name_workplace')
    def title_string_name_workplace(self):
        if self.name_workplace:
            self.name_workplace = self.name_workplace.title()
            
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
    def changue_rol_vocero_to_persons(self):
        self.is_vocero = False
        self.is_persona = True
        self.into_committee = False
        group_vocero = self.env['res.groups'].sudo().search([('name', '=', 'Vocero')])
        group_residente = self.env['res.groups'].sudo().search([('name', '=', 'Residente del Consejo Comunal')])
        list_group = []
        for group in self.user_id.groups_id:
            list_group.append(group.id)
        if group_vocero.id in list_group:
            list_group.remove(group_vocero.id)
        list_group.append(group_residente.id)
        self.user_id.sudo().write({'groups_id': [(6,0,list_group)]})
        committe = self.env['tcc.committee'].sudo().search([('communal_council_id', '=', self.communal_council_id.id),('active','=',True)])
        list_person = []
        for com in committe:
            for person in com.person_ids:
                list_person.append(person.id)
            if self.id in list_person:
                list_person.remove(self.id)
            committe.sudo().write({'person_ids': [(6,0,list_person)]})

    @api.multi
    def changue_rol_person_to_vocero(self):
        self.is_vocero = True
        self.is_persona = False
        self.into_committee = False
        group_vocero = self.env['res.groups'].sudo().search([('name', '=', 'Vocero')])
        group_residente = self.env['res.groups'].sudo().search([('name', '=', 'Residente del Consejo Comunal')])
        list_group = []
        for group in self.user_id.groups_id:
            list_group.append(group.id)
        if group_residente.id in list_group:
            list_group.remove(group_residente.id)
        list_group.append(group_vocero.id)
        self.user_id.sudo().write({'groups_id': [(6,0,list_group)]})

    @api.onchange('first_name')
    def title_first_name(self):
        if self.first_name:
            self.first_name = self.first_name.title()
    
    @api.onchange('is_family_boss')
    def claim_is_family_boss(self):
        if self.is_family_boss == True:
            self.kinship_id = False
    
    @api.onchange('second_name')
    def title_string_second_name(self):
        if self.second_name:
            self.second_name = self.second_name.title()
    
    @api.onchange('login')
    def lower_string_login(self):
        if self.login:
            self.login = self.login.lower()
            
    @api.onchange('first_surname')
    def title_string_first_surname(self):
        if self.first_surname:
            self.first_surname = self.first_surname.title()
            self.name = self.first_name +' '+ self.first_surname
            
    @api.onchange('second_surname')
    def title_string_second_surname(self):
        if self.second_surname:
            self.second_surname = self.second_surname.title()
        
    
    
class TccPersonsProfession(models.Model):
    _name = "tcc.persons.profession"
    _rec_name = 'name'
    _description = "Profesion de las personas"
    
    name = fields.Char(
                string='Nombre',
                required = True,
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "La Profesión ya Existe, Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccPersonsKinship(models.Model):
    _name = "tcc.persons.kinship"
    _rec_name = 'name'
    _description = "Parentesco familiar"
    
    name = fields.Char(
                string='Nombre',
                required = True,
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El Parentesco ya Existe. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()
