# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models
from odoo.tools import float_round


class report_communal_council_admin(models.AbstractModel):
    _name = 'report.tcc_communal_council.council_admin'

    @api.model
    def render_html(self, docids, data=None):
        data = data if data is not None else {}
        communals = self.env['tcc.communal.council'].browse(data.get('ids', data.get('active_ids')))
        docargs = {
            'doc_ids': data.get('ids', data.get('active_ids')),
            'doc_model': 'tcc.communal.council', 'tcc.family', 'tcc.person', 
            'docs': communals,
            'data': dict(
                data
            ),
        }
        return self.env['report'].render('tcc_communal_council.council_admin_template', docargs)

