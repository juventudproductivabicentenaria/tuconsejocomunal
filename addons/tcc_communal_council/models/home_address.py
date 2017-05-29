# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

class HomeAddressSector(models.Model):
    _name = "tcc.address.sector"
    _rec_name = 'name'
    _description = "Sector"
    
    
    name = fields.Char(
                string='Nombre del sector',
                required=True,
                )
    active = fields.Boolean(default=True)
    

class HomeAddressStreet(models.Model):
    _name = "tcc.address.street"
    _rec_name = 'name'
    _description = "Calle"
    
    
    name = fields.Char(
                string='Nombre o Número de la calle',
                required=True,
                )
    active = fields.Boolean(default=True)
    
