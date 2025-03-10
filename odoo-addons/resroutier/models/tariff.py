from odoo import models, fields

class Tariff(models.Model):
    _name = 'resroutier.tariff'
    _description = 'Calcul des tarifs de bus'

    route_id = fields.Many2one('resroutier.route', string='Ligne')
    price = fields.Float('Prix')