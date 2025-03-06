from odoo import models, fields

class Subscription(models.Model):
    _name = 'sts_front.subscription'
    _description = 'STS Subscription'

    name = fields.Char(string='Name', required=True)
    subscription_type = fields.Selection([
        ('semester', 'First Semester (15/09 - 15/12)'),
        ('annual', 'Annual (15/09 - 30/06)')
    ], string='Subscription Type', required=True)
    include_holidays = fields.Boolean(string='Include Holidays')
    route_id = fields.Many2one('resroutier.route', string='Route')