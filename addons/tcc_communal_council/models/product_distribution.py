# -*- coding: utf-8 -*-

from datetime import date, datetime
from datetime import * 
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
import math

class TccProductDistribution(models.Model):
    _name = "tcc.product.distribution"
    _rec_name = 'name'
    _description = 'Distribucion de productos'
    
    
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
                string="Nombre",
                required=True,
                states={'done': [('readonly', True)]},
                )
    
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                default=default_communal_council,
                readonly=True,
                )
    
    distribution_line_ids = fields.One2many(
                'tcc.product.distribution.line',
                'product_distribution_id',
                string='Lineas de Distribución',
                states={'done': [('readonly', True)]},
                )
    state = fields.Selection([
                ('draft', 'Borrador'),
                ('done', 'Confirmado'),
                ], string='Status', readonly=True, copy=False, index=True,
                )
    active = fields.Boolean(default=True)
    
    @api.onchange('name')
    def title_string(self):
        if self.name:
            self.name = self.name.title()
    
    @api.multi
    def action_confirm(self):
        vals = {}
        delivery_obj = self.env['tcc.distribution.delivery.confirmation']
        for distribution in self:
            vals = {
                'communal_council_id': distribution.communal_council_id.id,
                'product_distribution_id': distribution.id,
            }
            for line in distribution.distribution_line_ids:
                vals['response_id'] = line.response_id.id
                if line.to_deliver == 'familia':
                    for family in line.family_ids:
                        vals['family_id'] = family.id
                        delivery_obj.sudo().create(vals)
                if line.to_deliver == 'persona':
                    for person in line.person_ids:
                        vals['person_id'] = person.id
                        delivery_obj.sudo().create(vals)
            distribution.state = 'done'
        return True
    
    @api.model
    def create(self, vals):
        if not vals['distribution_line_ids']:
            raise UserError(_('Debe agregar Lineas de Distribución.'))
        distribution = super(TccProductDistribution, self).create(vals)
        distribution.update({
                'state': 'draft',
            })
        
        return distribution
    
class TccProductDistributionLine(models.Model):
    _name = "tcc.product.distribution.line"
    _rec_name = 'product_distribution_id'
    _description = 'Lineas de distribucion'
    
    
    product_distribution_id = fields.Many2one(
                'tcc.product.distribution',
                string='Distribución', 
                )
    response_id = fields.Many2one(
                'tcc.persons',
                string='Responsable', 
                domain = [('is_vocero', '=', True)],
                required = True,
                )
    to_deliver = fields.Selection(
                [('familia', 'Familias'),
                ('persona', 'Personas'),],
                string='Entregar a:', 
                required=True,
                )
    street_ids = fields.Many2many(
                'tcc.address.street',
                'tcc_product_distribution_line_street_rel',
                'distribution_id',
                'street_id',
                string='Calles'
                )
    date_start = fields.Datetime(
                string='Inicio de entrega',
                required=True,
                default=fields.Datetime.now,
                )
    date_end = fields.Datetime(
                string='Fin de entrega',
                required=True,
                #~ states={'draft': [('readonly', False)]},
                )
    family_ids = fields.Many2many(
                'tcc.family',
                'tcc_product_distribution_family_rel',
                'distribution_line_id',
                'family_id',
                string='Familias'
                )
    person_ids = fields.Many2many(
                'tcc.persons',
                'tcc_distribution_person_rel',
                'distribution_line_id',
                'person_id',
                string='Personas',
                )
    @api.model
    def create(self, vals):
        if not vals['family_ids'] and not vals['person_ids']:
            raise UserError(_('Debe Seleccionar las Familias o Personas Beneficiadas.'))
        DistributionLine = super(TccProductDistributionLine, self).create(vals)
        return DistributionLine
    
    @api.multi
    @api.onchange('street_ids')
    def families_domain(self):
        domain = {}
        list_street = []
        list_family = []
        list_person = []
        for street in self.street_ids:
            list_street.append(street.id)
        families = self.env['tcc.family'].search([('house_id.street_id.id', 'in', list_street)])
        for family in families:
            list_family.append(family.id)
            for person in family.person_ids:
                list_person.append(person.id)
        domain = {'family_ids': [('id','in',list_family)], 'person_ids': [('id','in',list_person)]}
        return {'domain': domain}
    
    
    @api.onchange('to_deliver')
    def onchangue_to_deliver(self):
        domain = {}
        list_street = []
        list_family = []
        if self.to_deliver == 'familia' or self.to_deliver == False:
            self.person_ids = False
        if self.to_deliver == 'persona' or self.to_deliver == False:
            self.family_ids = False
    
    @api.onchange('date_end')
    def to_validate_date(self):
        warning = {}
        result = {}
        if self.date_end:
            if cmp(self.date_end, self.date_start) == -1:
                warning = {
                    'title': _('Warning!'),
                    'message': _('La Fecha Final no debe ser menor a la Fecha de Inicio. ¡Verifique!'),
                }
                self.date_end = False
                if warning:
                    result['warning'] = warning
            return result

class TccProductDistributionConfirm(models.Model):
    _name = "tcc.distribution.delivery.confirmation"
    _rec_name = 'response_id'
    _description = 'Confirmacion de entrega'
    
    
    communal_council_id = fields.Many2one(
                'tcc.communal.council',
                string='Consejo comunal', 
                readonly=True,
                )
    family_id = fields.Many2one(
                'tcc.family',
                string='Familia', 
                readonly=True,
                )
    person_id = fields.Many2one(
                'tcc.persons',
                string='Persona',
                readonly=True, 
                )
    date_delivery = fields.Datetime(
                string='Fecha de entrega',
                readonly=True,
                #~ states={'draft': [('readonly', False)]},
                )
    response_id = fields.Many2one(
                'tcc.persons',
                string='Responsable', 
                domain = [('is_vocero', '=', True)],
                readonly=True,
                )
    product_distribution_id = fields.Many2one(
                'tcc.product.distribution',
                string='Nombre', 
                )
    state = fields.Selection([
        ('por_entregar', 'Por Entregar'),
        ('entregado', 'Entregado'),
        ], string='Status', readonly=True, copy=False, index=True, default = 'por_entregar'
        )
    active = fields.Boolean(default=True)
    
    
    @api.multi
    def action_confirm_delivery(self):
        self.sudo().write({'state': 'entregado', 'date_delivery': fields.Datetime.now()})
        return True
