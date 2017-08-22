# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

class HomeAddressSector(models.Model):
    _name = "tcc.address.sector"
    _rec_name = 'name'
    _description = "Sector"
    
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
                default= default_communal_council,
                readonly=True,
                )
    municipality_id = fields.Many2one(
                'res.country.state.municipality', 
                string='Municipio',
                #~ readonly=True,
                )
    parish_id = fields.Many2one(
                'res.country.state.municipality.parish',
                string='Parroquia', 
                required=True,
                )
    name = fields.Char(
                string='Nombre del sector',
                required=True,
                )
    active = fields.Boolean(default=True)
    
    
    @api.onchange('municipality_id')
    def default_municipio(self):
        if not self.municipality_id:
            self.municipality_id = self.communal_council_id.municipality_id.id
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()


class HomeAddressStreet(models.Model):
    _name = "tcc.address.street"
    _rec_name = 'name'
    _description = "Calle"
    
    
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
    sector_id = fields.Many2one(
                'tcc.address.sector',
                string='Sector', 
                )
    name = fields.Char(
                string='Nombre o Número de la calle',
                required=True,
                )
    active = fields.Boolean(default=True)
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()
