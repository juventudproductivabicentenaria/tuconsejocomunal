# -*- coding: utf-8 -*-

from odoo import api, fields, models


class WizardReportCommunalCouncilAdmin(models.TransientModel):
    _name = "tcc.wizard_communal_council_admin"
    _description = "Communal Council Admin Wizard Report"

    title=fields.Char('Titulo',required=True)
    description=fields.Text('Descripción',required=True)
    date_init=fields.Date('Fecha')
    
	@api.multi
	def next(self):
		attrs="{'invisible': [('title','='true')]}"
		attrs="{'invisible': [('description','='true')]}"
		attrs="{'invisible': [('date_init','='true')]}"
    @api.multi
    def action_report(self):
        """Metodo que llama la lógica que genera el reporte"""
        datas={'ids': self.env.context.get('active_ids', [])}
        res = self.read(['title', 'description', 'date_init'])
        res = res and res[0] or {}
        datas['form'] = res
        domain=[]
        if self.date_init:
            domain=[('create_date','<',self.date_init)]
        fields=['name','creation_date','state_id']
        communals_data = self.env['tcc.communal.council'].search_read(domain,fields)
        datas['communals_data'] = communals_data
        return self.env['report'].get_action([], 'tcc_communal_council.council_admin', data=datas)
    
    
