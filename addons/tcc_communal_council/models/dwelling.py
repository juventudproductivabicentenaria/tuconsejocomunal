# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError


class Dwelling(models.Model):
    _name = "tcc.dwelling"
    _rec_name = 'communal_council_id'
    _description = "Vivienda"
    
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
    
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                default=default_communal_council,
                readonly=True,
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
                string='Edificios',
                help="Edificios ubicados en el sector del Consejo comunal.",
                )
    active = fields.Boolean(default=True)


class DwellingHouse(models.Model):
    _name = "tcc.dwelling.house"
    _rec_name = 'name'
    _description = "Casas"
    
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
    
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                default=default_communal_council,
                readonly=True,
                )
    name = fields.Char(
                string='Nombre o número de la casa',
                required=True,
                )
    dwelling_id = fields.Many2one(
                'tcc.dwelling',
                string='Vivienda', 
                )
    sector_id = fields.Many2one(
                'tcc.address.sector',
                string='Sector', 
                required=True,
                )
    street_id = fields.Many2one(
                'tcc.address.street',
                string='Calle', 
                required=True,
                )
    active = fields.Boolean(default=True)
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()
    
class DwellingEdifice(models.Model):
    _name = "tcc.dwelling.edifice"
    _rec_name = 'name'
    _description = "Edificio"
    
    
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
    
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                default=default_communal_council,
                readonly=True,
                )
    
    name = fields.Char(
                string='Nombre o número del edificio',
                required=True,
                )
    dwelling_id = fields.Many2one(
                'tcc.dwelling',
                string='Vivienda', 
                )
    sector_id = fields.Many2one(
                'tcc.address.sector',
                string='Sector', 
                required=True,
                )
    street_id = fields.Many2one(
                'tcc.address.street',
                string='Calle', 
                required=True,
                )
    active = fields.Boolean(default=True)
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()
