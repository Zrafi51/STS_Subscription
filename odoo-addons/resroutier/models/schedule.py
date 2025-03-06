from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Schedule(models.Model):
    _name = 'resroutier.schedule'
    _description = 'Route Schedule'
    _order = 'departure_time'

    route_id = fields.Many2one('resroutier.route', string='Route', required=True)
    departure_time = fields.Float(string='Departure Time', required=True)
    arrival_time = fields.Float(string='Arrival Time', required=True)

    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekday', 'Weekdays Only'),
        ('weekend', 'Weekends Only')
    ], string='Frequency', default='daily', required=True)

    @api.constrains('departure_time', 'arrival_time')
    def _check_times(self):
        for schedule in self:
            if schedule.departure_time >= schedule.arrival_time:
                raise ValidationError('Departure time must be before arrival time')