# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class Family(models.Model):
    _name = "tcc.family"
    _rec_name = 'name'
    
    @api.multi
    def default_communal_council(self):
        list_group_name = []
        for name_goup in self.env.user.groups_id:
            list_group_name.append(name_goup.name)
        print list_group_name
        if 'Consejo Comunal' in list_group_name:
            return self.env['tcc.communal.council'].search([('user_id', '=', self.env.uid)]).id
        #~ elif 'Vocero' in list_group_name:
            #~ print 0000
            #~ print 0000
            #~ print 0000
            #~ print 0000
    
    _tenancy_data=[
                ('Propia', 'Propia'),
                ('Alquilada', 'Alquilada'),
                ('Invadida','Invadida'),
                ('Adjudicada','Adjudicada'),
                ]
    _type_dwelling_data=[
                ('Casa', 'Casa'),
                ('Apartamento', 'Apartamento'),
                ]

    name = fields.Char(
                string='Nombre de la familia',
                )
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                default=default_communal_council,
                )
    apartment_id = fields.Many2one(
                'tcc.family.apartment',
                string='Apartamento', 
                )
    floor_id = fields.Many2one(
                'tcc.family.apartment.floor',
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
                _tenancy_data, 
                string='Tenencia de vivienda', 
                default='Propia',
                )
    type_dwelling = fields.Selection(
                _type_dwelling_data, 
                string='Tipo de Vivienda', 
                default='Casa',
                )
    arrival_date = fields.Date(
                string='Fecha de llegada',
                index=True,
                )
    active = fields.Boolean(default=True)

    
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
    
    @api.multi
    @api.onchange('house_id')
    def house_id_change_domain(self):
        domain = {}
        list_house_id = []
        dwelling = self.env['tcc.dwelling'].search([('communal_council_id', '=', int(self.communal_council_id.id))])
        for dw in dwelling:
            for house in dw.house_ids:
                list_house_id.append(house.id)
        #~ list_house_id = [(2,3)]
        #~ print list_house_id
        #~ print list_house_id
        #~ print list_house_id
        #~ print list_house_id
        #~ print list_house_id
        for list_house in list_house_id:
            print list_house
            print list_house
            print list_house
            #~ domain['house_id'] = [('house_id','=',list_house)]
        #~ domain = {'house_id': list_house_id}
        return {'domain': domain}
        
    
class FamilyApartment(models.Model):
    _name = "tcc.family.apartment"
    _rec_name = 'name'
    
    name = fields.Char(
                string='Nombre o número del apartamento',
                )
    active = fields.Boolean(default=True)


class FamilyApartmentFloor(models.Model):
    _name = "tcc.family.apartment.floor"
    _rec_name = 'name'
    
    name = fields.Char(
                string='Nombre o número del Piso',
                )
    active = fields.Boolean(default=True)
