# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
import math

class TccDelivery(models.Model):
    _name = "tcc.product.distribution"
    _rec_name = 'name'
    _description = 'Distribucion de productos'
    
    
    @api.multi
    def range_edad(self):
        list_age = []
        for num in range(0, 150):
            list_age.append((str(num),str(num)))
        return list_age
    
    @api.multi
    def default_communal_council(self):
        list_group_name = []
        for name_goup in self.env.user.groups_id:
            list_group_name.append(name_goup.name)
        if 'Consejo Comunal' in list_group_name:
            return self.env['tcc.communal.council'].search([('user_id', '=', self.env.uid)]).id
        if 'Vocero' in list_group_name:
            return self.env['tcc.communal.council'].search([('communal_council_id.user_id', '=', self.env.uid)]).id
        if 'Residente del Consejo Comunal' in list_group_name:
            return self.env['tcc.communal.council'].search([('communal_council_id.user_id', '=', self.env.uid)]).id
    
    name = fields.Char(
                string="Nombre",
                required=True,
                )
    
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                default=default_communal_council,
                )
    to_deliver = fields.Selection(
                [('familia', 'Familias'),
                ('persona', 'Personas'),],
                string='Entregar a:', 
                required=True,
                )
    distribute_by = fields.Selection(
                [('familia', 'Familia'),
                ('casa', 'Casa'),
                ('calle', 'Calle'),],
                string='Distribuir por:', 
                required=True,
                )
    age_start = fields.Selection(
                range_edad,
                string='Edad inicial', 
                default = 0
                )
    age_end = fields.Selection(
                range_edad,
                string='Edad final', 
                )
    estimated_time = fields.Char(
                string="Tipo estimado",
                required=True,
                help="Tiempo estimado por entrega, basandose en horas."
                )
    street_id = fields.Many2one(
                'tcc.address.street',
                string='Calle', 
                )
    street_ids = fields.Many2many(
                'tcc.address.street',
                'tcc_product_distribution_street_rel',
                'distribution_id',
                'street_id',
                string='Calles'
                )
    family_ids = fields.Many2many(
                'tcc.family',
                'tcc_product_distribution_family_rel',
                'distribution_id',
                'family_id',
                string='Familias'
                )
                
    active = fields.Boolean(default=True)
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()
    
    @api.onchange('to_deliver')
    def clean_fields(self):
        if self.to_deliver == False or 'familia':
            self.age_start = False
            self.age_end = False
    
    @api.onchange('age_start')
    def clean_fields_age_end(self):
        self.age_end = False
    
    @api.onchange('age_end')
    def validate_age(self):
        warning = {}
        result = {}
        if self.age_end:
            print self.age_start
            print self.age_end
            if self.age_start:
                if int(self.age_start) > int(self.age_end):
                    warning = {
                        'title': _('Warning!'),
                        'message': _('La edad inicial no debe ser mayor a la edad final.'),
                    }
                    self.age_end = False
                    if warning:
                        result['warning'] = warning
                    return result
            else:
                warning = {
                        'title': _('Warning!'),
                        'message': _('Seleccione la inicial. ¡Verifique!'),
                    }
                self.age_end = False
                if warning:
                    result['warning'] = warning
                return result
    
    @api.onchange('estimated_time')
    def validate_estimated_time(self):
        if self.estimated_time:
            warning = {}
            result = {}
            if '_' in self.estimated_time:
                warning = {
                            'title': _('Warning!'),
                            'message': _('Completa el formato  del campo tiempo estimado con cero (0) al inicio.'),
                        }
                self.estimated_time = False
                if warning:
                    result['warning'] = warning
                return result
