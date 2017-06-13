# -*- coding: utf-8 -*-

import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import float_compare, float_is_zero


class TccNoticias(models.Model):
    _name = 'tcc.notice'
    _description = 'Noticias del Consejo Comunal'
    _rec_name = 'name'
    
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                )
    category_id = fields.Many2one(
                'tcc.notice.category',
                string='Categoría', 
                )
    name = fields.Char(
                string='Título',
                required = True,
                )
    subtitle = fields.Char(
                string='Subtítulo',
                required = True,
                )
    start_date = fields.Date(
                string='Fecha de Inicio',
                )
    end_date = fields.Date(
                string='Fecha final',
                )
    sumary = fields.Html(
                'Descripción',
                required=True,
                )
    active = fields.Boolean(default=True)
    
    @api.onchange('name')
    def upper_string(self):
        if self.name:
            self.name = self.name.upper()

    @api.onchange('subtitle')
    def title_string(self):
        if self.subtitle:
            self.subtitle = self.subtitle.title()

class TccNoticiasCategoria(models.Model):
    _name = 'tcc.notice.category'
    _description = 'Categoria de Noticias'
    _rec_name = 'name'
    
    
    name = fields.Char(
                string='Categoría',
                required = True,
                )
    active = fields.Boolean(default=True)
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()
