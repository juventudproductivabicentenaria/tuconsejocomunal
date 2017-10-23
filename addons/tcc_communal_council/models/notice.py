# -*- coding: utf-8 -*-

import re
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
    
    @api.multi
    def metodo_ejemplo(self):
        return self.search_count([('state','=','done')])
    
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
    state = fields.Selection([
                ('draft', 'Borrador'),
                ('done', 'Publicado'),
                ], string='Status', readonly=True, copy=False, index=True,default=False
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
    
    @api.multi
    def publish_notice(self):
        self.state = 'done'
    @api.multi
    def strip_tags(self,value):
        return re.sub(r'<[^>]*?>', '', value)
    
    @api.model
    def create(self,vals):
        vals.update({'state': 'draft'})
        sumary=self.strip_tags(vals['sumary'])
        if not sumary:
            raise UserError(_('Debe redactar el cuerpo de la noticia.'))
        return super(TccNoticias, self).create(vals)
    
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
            
    
