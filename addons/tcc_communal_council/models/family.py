# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.http import request

import uuid
import urlparse

class TccFamily(models.Model):
    _name = "tcc.family"
    _rec_name = 'name'
    _description = 'Familia'
    
    
    @api.multi
    def action_start_survey(self):
        """ Open the website page with the survey form """
        survey = self.env['survey.survey'].search([('tcc_survey', '=', True)])
        survey.ensure_one()
        self.survey_defaul = True
        token = survey.env.context.get('survey_token')
        trail = "/%s" % token if token else ""
        
        users = 0
        for person in self.person_ids:
            if person.is_family_boss == True:
                users = person.user_id.partner_id.id
        tcc = "/%s" % users +"-tcc"
        return {
            'type': 'ir.actions.act_url',
            'name': "Start Survey",
            'target': 'self',
            'url': survey.with_context(relative_url=True).public_url + tcc,
        }
    
    
    @api.multi
    def send_survey(self):
        
        """ Open a window to compose an email, pre-filled with the survey message """
        users = []
        self.survey_defaul = True
        for person in self.person_ids:
            if person.is_family_boss == True:
                users.append(person.user_id.partner_id.id)
        
        survey = self.env['survey.survey'].search([('tcc_survey', '=', True)])
        # Ensure that this survey has at least one page with at least one question.
        if not survey.page_ids or not [page.question_ids for page in survey.page_ids if page.question_ids]:
            raise UserError(_('No puedes enviar una encuesta sin preguntas..'))

        if survey.stage_id.closed:
            raise UserError(_("No puedes realizar invitaciones de encuentas Cerradas."))

        template = survey.env.ref('survey.email_template_survey', raise_if_not_found=False)

        local_context = dict(
            survey.env.context,
            default_model='survey.survey',
            default_res_id=survey.id,
            default_survey_id=survey.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            default_partner_ids = [(6,0,users)],
        )
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'survey.mail.compose.message',
            'target': 'new',
            'context': local_context,
        }
    
        
    @api.multi
    def default_communal_council(self):
        list_group_name = []
        for name_goup in self.env.user.groups_id:
            list_group_name.append(name_goup.name)
        if 'Consejo Comunal' in list_group_name:
            return self.env['tcc.communal.council'].search([('user_id', '=', self.env.uid)]).id
        if 'Vocero' in list_group_name:
            return self.env['tcc.communal.council'].search([('communal_council_id.user_id', '=', self.env.user.communal_council_id.user_id.id)]).id
        if 'Residente del Consejo Comunal' in list_group_name:
            return self.env['tcc.communal.council'].search([('communal_council_id.user_id', '=', self.env.uid)]).id
                
                
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()
    
    
    
    tenancy_data=[
                ('Propia', 'Propia'),
                ('Alquilada', 'Alquilada'),
                ('Compartida','Compartida'),
                ('Invadida','Invadida'),
                ('Traspasada','Traspasada'),
                ('Prestada','Prestada'),
                ('Other','Otro'),
                ]
    type_dwelling_data=[
                ('Quinta', 'Quinta'),
                ('Casa', 'Casa'),
                ('Apartamento', 'Apartamento'),
                ('Rancho', 'Rancho'),
                ('Barraca', 'Barraca'),
                ('Habitacion', 'Habitación'),
                ('Other','Otro'),
                ]
    
    
    name = fields.Char(
                string='Nombre de la familia',
                readonly=True,
                )
    code_family = fields.Char(
                string='Código de la familia',
                readonly=True,
                )
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                default=default_communal_council,
                readonly=True,
                )
    apartment = fields.Char(
                string='Apartamento',
                )
    floor = fields.Char(
                string='Piso',
                )
    house_id = fields.Many2one(
                'tcc.dwelling.house',
                string='Casa', 
                )
    edifice_id = fields.Many2one(
                'tcc.dwelling.edifice',
                string='Edificio', 
                )
    tenancy = fields.Selection(
                tenancy_data, 
                string='Forma de Tenencia', 
                default='Propia',
                )
    type_dwelling = fields.Selection(
                type_dwelling_data, 
                string='Tipo de Vivienda', 
                default='Casa',
                )
    terreno_propio = fields.Selection(
                [('Si', 'Si'),
                ('No', 'No'),],
                string='Terreno propio', 
                )
    pertenece_ocv = fields.Selection(
                [('Si', 'Si'),
                ('No', 'No'),],
                string='Pertenece a (OCV)', 
                )
    type_walls_ids = fields.Many2many(
                'tcc.family.type.walls',
                'tcc_family_type_walls_rel',
                'family_id',
                'type_walls_id',
                string='Tipo de pared'
                )
    type_roof_ids = fields.Many2many(
                'tcc.family.type.roof',
                'tcc_family_type_roof_rel',
                'family_id',
                'type_roof_id',
                string='Tipo de techo'
                )
    equipment_dwelling_ids = fields.Many2many(
                'tcc.family.dwelling.equipment',
                'tcc_family_equipment_dwelling_rel',
                'family_id',
                'equipment_id',
                string='Enseres de la vivienda'
                )
    salubrity_id = fields.Many2one(
                'tcc.family.dwelling.salubrity',
                string='Salud de vivienda', 
                )
    pests_dwelling_ids = fields.Many2many(
                'tcc.family.dwelling.pests',
                'tcc_family_dwelling_pests_rel',
                'family_id',
                'pest_id',
                string='Insectos y roedores'
                )
    pets_ids = fields.Many2many(
                'tcc.family.dwelling.pets',
                'tcc_family_dwelling_pets_rel',
                'family_id',
                'pest_id',
                string='Animales domésticos'
                )
    room_ids = fields.Many2many(
                'tcc.family.dwelling.room',
                'tcc_family_dwelling_room_rel',
                'family_id',
                'room_id',
                string='Habitaciones en la vivienda'
                )
    cant_room = fields.Integer(string='cantidad de habitaciones', )
    disease_ids = fields.Many2many(
                'tcc.family.disease',
                'tcc_family_disease_rel',
                'family_id',
                'disease_id',
                string='Enfermedades en la familia'
                )
    need_help = fields.Selection(
                [('Si', 'Si'),
                ('No', 'No'),],
                string='Necesita ayuda', 
                help="Necesita ayuda para familiares enfermos"
                )
    name_help = fields.Char(
                string='¿Cuáles ayudas?',
                )
    commercial_activity_hose = fields.Selection(
                [('Si', 'Si'),
                ('No', 'No'),],
                string='Actividad commercial en la vivienda', 
                )
    commercial_activity_ids = fields.Many2many(
                'tcc.family.commercial.activity',
                'tcc_family_commercial_activity_rel',
                'family_id',
                'commercial_activity_id',
                string='Venta de:'
                )
    family_income_id = fields.Many2one(
                'tcc.family.income',
                string='Ingreso familiar', 
                )
    arrival_date = fields.Date(
                string='Fecha de llegada a la comunidad',
                required=True,
                )
    person_ids = fields.One2many(
                'tcc.persons',
                'family_id',
                string='Grupo familiar',
                help="Casas ubicadas en el sector del Consejo comunal.",
                )
    children_street = fields.Boolean(
                default=False,
                string='Niños en la calle'
                )
    quantity_children_street = fields.Integer(
                string='¿Cuántos niños?', 
                )
    indigent = fields.Boolean(
                default=False,
                string='Indigentes'
                )
    quantity_indigent = fields.Integer(
                string='¿Cuántos indigentes?',
                 )
    terminally_patient = fields.Boolean(
                default=False,
                string='Enfermos terminales'
                )
    quantity_terminally_patient = fields.Integer(
                string='¿Cuántos enfermos terminales?',
                 )
    handicapped = fields.Boolean(
                default=False,
                string='Discapacitados'
                )
    quantity_handicapped = fields.Integer(
                string='¿Cuántos Discapacitados?',
                 )
    water_white_ids = fields.Many2many(
                'tcc.family.white.water',
                'tcc_family_white_water_rel',
                'family_id',
                'water_id',
                string='Aguas Blancas'
                )
    water_meter = fields.Boolean(
                string='Medidor de agua',
                )
    wastewater_ids = fields.Many2many(
                'tcc.family.waste.water',
                'tcc_family_waste_water_rel',
                'family_id',
                'wastewater_id',
                string='Aguas Residuales',
                )
    gas = fields.Selection(
                [('Bombona', 'Bombona'),
                ('Tuberia', 'Tubería'),
                ('no_posee', 'No posee'),],
                string='Gas', 
                help="¿Cómo es el sistema de distribución de gas en su vivienda?"
                )
    electric_system = fields.Selection(
                [('publica', 'Electricidad Pública'),
                ('planta_electrica', 'Planta Eléctrica Propia'),
                ('no_posee', 'No Posee'),],
                string='Tipo de electricidad', 
                help="¿Cómo es el sistema de distribución de electricidad en su vivienda?"
                )
    light_meter = fields.Boolean(
                string='Medidor de luz',
                )
    trash_ids = fields.Many2many(
                'tcc.family.collect.trash',
                'tcc_family_collect_trash_rel',
                'family_id',
                'trash_id',
                string='Recolección de basura'
                )
    telephony_ids = fields.Many2many(
                'tcc.family.services.telephony',
                'tcc_family_services_telephony_rel',
                'family_id',
                'telephony_id',
                string='Tipo de telefonía'
                )
    transport_ids = fields.Many2many(
                'tcc.family.services.transport',
                'tcc_family_services_transport_rel',
                'family_id',
                'transport_id',
                string='Tipo de transporte'
                )
    media_ids = fields.Many2many(
                'tcc.family.services.media',
                'tcc_family_services_media_rel',
                'family_id',
                'media_id',
                string='Medios de información'
                )
    survey_defaul = fields.Boolean(default=False,string="Encuestado")
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El jefe de familia ya se encuentra registrado. ¡Verifique!")]
    
    @api.multi
    @api.constrains('person_ids')
    def get_name_family(self):
        list_family_boss = []
        name_person = ''
        for person in self.person_ids:
            list_group = []
            #~ if family.person_ids:
                #~ for person in family.person_ids:
            group_contact = self.env['res.groups'].sudo().search([('name', '=', 'Creación de contactos')])
            list_group.append(group_contact.id)
            group_employee = self.env['res.groups'].sudo().search([('name', '=', 'Empleado')])
            list_group.append(group_employee.id)
            if person.user_id.is_vocero == True:
                group_vocero = person.env['res.groups'].sudo().search([('name', '=', 'Vocero')])
                list_group.append(group_vocero.id)
                person.user_id.sudo().write({'is_vocero': True, 'is_persona': False,'groups_id' : [(6,0,list_group)],'email' : person.user_id.login})
            else:
                group_residente = person.env['res.groups'].sudo().search([('name', '=', 'Residente del Consejo Comunal')])
                list_group.append(group_residente.id)
                person.user_id.sudo().write({'is_persona': True, 'is_vocero': False, 'groups_id' : [(6,0,list_group)],'email' : person.user_id.login})
            #~ else:
                #~ raise UserE
            
            
            
            
            if person.is_family_boss == True:
                name_person = person.name +' '+ person.cedula
                list_family_boss.append(person.id)
            if len(list_family_boss) != 1:
                raise ValidationError(_('Un grupo familiar, debe tener un jefe de familia. ¡Verifique!'))
            else:
                self.name = name_person
            
            
            
            
    
    @api.onchange('arrival_date')
    def to_validate_date(self):
        warning = {}
        result = {}
        if self.arrival_date:
            if cmp(datetime.strptime(self.arrival_date, DF).date(), date.today()) == 1:
                warning = {
                    'title': _('Warning!'),
                    'message': _('La fecha seleccionada no debe ser mayor a la fecha de hoy.'),
                }
                self.arrival_date = False
                if warning:
                    result['warning'] = warning
            return result
    
    
    
    
    @api.onchange('type_dwelling')
    def onchange_type_dwelling(self):
        if self.type_dwelling == False:
            self.house_id = False
        if self.type_dwelling != 'Apartamento':
            self.edifice_id = False
            self.apartment = False
            self.floor = False
        else:
            self.house_id = False
            
    @api.onchange('need_help')
    def no_help(self):
        if self.need_help != 'Si':
            self.name_help = False
    
    @api.onchange('children_street')
    def no_children_street(self):
        if self.children_street == False:
            self.quantity_children_street = False
    
    @api.onchange('indigent')
    def no_indigent(self):
        if self.indigent == False:
            self.quantity_indigent = False
    
    @api.onchange('terminally_patient')
    def no_terminally_patient(self):
        if self.terminally_patient == False:
            self.quantity_terminally_patient = False
    
    @api.onchange('handicapped')
    def no_handicapped(self):
        if self.handicapped == False:
            self.quantity_handicapped = False
    
    @api.onchange('electric_system')
    def no_electric_system(self):
        if self.electric_system == False or self.electric_system == 'no_posee':
            self.light_meter = False
    
    
    @api.onchange('name_help')
    def title_string_name_help(self):
        if self.name_help:
            self.name_help = self.name_help.title()
    
    @api.onchange('apartment')
    def apartament_upper(self):
        if self.apartment:
            self.apartment = self.apartment.upper()
    
    @api.onchange('floor')
    def floor_upper(self):
        if self.floor:
            self.floor = self.floor.upper()
    
    @api.model
    def create(self, vals):
        vals['code_family'] = self.env['ir.sequence'].next_by_code('tcc.family')
        family = super(TccFamily, self).create(vals)
        family.get_name_family()
        #~ list_group = []
        #~ if family.person_ids:
            #~ for person in family.person_ids:
                #~ group_contact = person.env['res.groups'].sudo().search([('name', '=', 'Creación de contactos')])
                #~ list_group.append(group_contact.id)
                #~ group_employee = person.env['res.groups'].sudo().search([('name', '=', 'Empleado')])
                #~ list_group.append(group_employee.id)
                #~ if person.user_id.is_vocero == True:
                    #~ group_vocero = person.env['res.groups'].sudo().search([('name', '=', 'Vocero')])
                    #~ list_group.append(group_vocero.id)
                    #~ person.user_id.sudo().write({'is_vocero': True, 'groups_id' : [(6,0,list_group)],'email' : person.user_id.login})
                #~ else:
                    #~ group_residente = person.env['res.groups'].sudo().search([('name', '=', 'Residente del Consejo Comunal')])
                    #~ list_group.append(group_residente.id)
                    #~ person.user_id.sudo().write({'is_persona': True, 'groups_id' : [(6,0,list_group)],'email' : person.user_id.login})
        #~ else:
            #~ raise UserError(_('Debe agregar pesonas al grupo familiar.'))
        return family 
        
        
    

class FamilyCommercialActivity(models.Model):
    _name = "tcc.family.commercial.activity"
    _rec_name = 'name'
    _description = 'Actividad comercial familiar'
    
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "La actividad comercial ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyIncome(models.Model):
    _name = "tcc.family.income"
    _rec_name = 'name'
    _description = 'Ingreso familiar'
    
    name = fields.Char(
                string='Ingreso familiar',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El Ingreso familiar ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()
    


class TccFamilyTypeWalls(models.Model):
    _name = "tcc.family.type.walls"
    _rec_name = 'name'
    _description = 'Tipo de paredes'
    
    name = fields.Char(
                string='Tipo de pared',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El tipo de pared ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyTypeRoof(models.Model):
    _name = "tcc.family.type.roof"
    _rec_name = 'name'
    _description = 'Tipo de techo'
    
    name = fields.Char(
                string='Tipo de techo',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El tipo de techo ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyDwellingEquipment(models.Model):
    _name = "tcc.family.dwelling.equipment"
    _rec_name = 'name'
    _description = 'Enseres de la vivienda'
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El nombre del enser ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyDwellingSalubrity(models.Model):
    _name = "tcc.family.dwelling.salubrity"
    _rec_name = 'name'
    _description = 'Salubrity de la vivienda'
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El nombre ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyDwellingPests(models.Model):
    _name = "tcc.family.dwelling.pests"
    _rec_name = 'name'
    _description = 'Plagas en la vivienda'
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El nombre ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyDwellingPets(models.Model):
    _name = "tcc.family.dwelling.pets"
    _rec_name = 'name'
    _description = 'Animales domesticos'
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El Nombre ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyDwellingRoom(models.Model):
    _name = "tcc.family.dwelling.room"
    _rec_name = 'name'
    _description = 'Habitaciones en la vivienda'
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El nombre ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyDisease(models.Model):
    _name = "tcc.family.disease"
    _rec_name = 'name'
    _description = 'Enfermedades en la familia'
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El nombre ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyWhiteWater(models.Model):
    _name = "tcc.family.white.water"
    _rec_name = 'name'
    _description = 'Tipos de aguas blancas'
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El nombre ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyWasteWater(models.Model):
    _name = "tcc.family.waste.water"
    _rec_name = 'name'
    _description = 'Aguas servidas'
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El nombre ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyCollectTrash(models.Model):
    _name = "tcc.family.collect.trash"
    _rec_name = 'name'
    _description = 'Recoleccion de basura'
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El nombre ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyServicesTelephony(models.Model):
    _name = "tcc.family.services.telephony"
    _rec_name = 'name'
    _description = 'Servicio de telefonia'
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El nombre ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyServicesTransport(models.Model):
    _name = "tcc.family.services.transport"
    _rec_name = 'name'
    _description = 'Servicio de trnsporte'
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El nombre ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class TccFamilyServicesMedia(models.Model):
    _name = "tcc.family.services.media"
    _rec_name = 'name'
    _description = 'Medios de informacion'
    
    name = fields.Char(
                string='Nombre',
                )
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El nombre ya se encuentra registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


