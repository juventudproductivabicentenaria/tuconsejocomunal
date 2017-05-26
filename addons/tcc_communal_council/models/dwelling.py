# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

class Dwelling(models.Model):
    _name = "tcc.dwelling"
    _rec_name = 'name'
    _description = "Vivienda"
    
    def default_communal_council(self):
        list_group_name = []
        for name_goup in self.env.user.groups_id:
            list_group_name.append(name_goup.name)
        print list_group_name
        if 'Consejo Comunal' in list_group_name:
            return self.env['tcc.communal.council'].search([('user_id', '=', self.env.uid)]).id
    
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                default=default_communal_council,
                )
    house_ids = fields.One2many(
                'tcc.dwelling.house',
                'dwelling_id',
                string='Casas',
                help="Casas ubicadas en el sector del Consejo comunal.",
                )
    edifice_ids = fields.One2many(
                'tcc.dwelling.edifice',
                'dwelling_id',
                string='Casas',
                help="Edificios ubicadas en el sector del Consejo comunal.",
                )
    active = fields.Boolean(default=True)

class DwellingHouse(models.Model):
    _name = "tcc.dwelling.house"
    _rec_name = 'name'
    _description = "Casas"
    
    name = fields.Char(
                string='Nombre de la casa',
                )
    number = fields.Integer(
                string='Numero de la casa',
                )
    dwelling_id = fields.Many2one(
                'tcc.dwelling',
                string='Vivienda', 
                default=default_communal_council,
                )
