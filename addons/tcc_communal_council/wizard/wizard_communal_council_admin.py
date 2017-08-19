# -*- coding: utf-8 -*-

from odoo import api, fields, models


class WizardReportCommunalCouncilAdmin(models.TransientModel):
    _name = "tcc.wizard.communal.council.admin"
    _description = "Communal Council Admin Wizard Report"

    title=fields.Char('Titulo',required=True)
    description=fields.Text('Descripción',required=True)
    date_init=fields.Date('Fecha')

    @api.multi
    def action_report(self):
        """Metodo que llama la lógica que genera el reporte"""
        return True
    
