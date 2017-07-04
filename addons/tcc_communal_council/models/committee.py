# -*- coding: utf-8 -*-

from datetime import * 


import calendar

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class TccCommittee(models.Model):
    _name = 'tcc.committee'
    _description = "Comites o Unidades"
    
    
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
    
    name = fields.Char(
                string='Nombre',
                required = True,
                )
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                default=default_communal_council,
                readonly=True,
                )
    person_ids = fields.Many2many(
                'tcc.persons',
                'tcc_committee_persons_rel',
                'committee_id',
                'person_id',
                string='Voceros',
                )
    
    active = fields.Boolean(default=True)
    
    _sql_constraints = [('name_uniq', 'unique (name)', "El comité ya está registrado. ¡Verifique!")]
    
    @api.onchange('name')
    def title_string_name(self):
        if self.name:
            self.name = self.name.title()
    
    @api.multi
    @api.constrains('person_ids')
    def validate_vocero(self):
        list_vocero = []
        if self.person_ids:
            for person in self.person_ids:
                list_vocero.append(person.id)
            if len(list_vocero) > 5:
                raise ValidationError(_('Un comité no puede tener más de Cinco (5) integrantes. ¡Verifique!'))
            else:
                vocero_lines = self.env['tcc.persons'].search([('id', '=', list_vocero)])
                vocero_lines.write({'into_committee': True})
        else:
            raise ValidationError(_('Debe seleccionar un vocero para el comité. ¡Verifique!'))
    
    @api.multi
    def write(self, values):
        list_person = []
        for p_id in self.person_ids:
            if p_id.id not in values['person_ids'][0][2]:
                list_person.append(p_id.id)
        PersonObj = self.env['tcc.persons'].search([('id', '=', list_person)])
        PersonObj.write({'into_committee': False})
        return super(TccCommittee, self).write(values)
    
