from openerp import models, fields, api

class res_partner(models.Model):

    _inherit = 'res.partner'

    municipality_id = fields.Many2one('res.country.state.municipality', 'Municipality')
    parish_id = fields.Many2one('res.country.state.municipality.parish', 'Parish')

    @api.model
    def _address_fields(self):
        address_fields = set(super(res_partner, self)._address_fields())
        address_fields.add('municipality_id')
        address_fields.add('parish_id')
        return list(address_fields)

