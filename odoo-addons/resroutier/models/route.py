from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Route(models.Model):
    _name = 'resroutier.route'
    _description = 'Bus Routes'

    route_name = fields.Char(string='Route Name', required=True)
    departure_stop_id = fields.Many2one('resroutier.stop', string='Departure Stop', required=True)
    arrival_stop_id = fields.Many2one('resroutier.stop', string='Arrival Stop', required=True)
    distance = fields.Float(string='Distance (km)', compute='_compute_distance', store=True)
    tariff = fields.Float(string='Base Tariff', compute='_compute_tariff', store=True)
    centre_exploitation = fields.Char(string='Card Receiving Point', required=True)
    
    # Additional fields for better route management
    schedule_ids = fields.One2many('resroutier.schedule', 'route_id', string='Schedules')
    notes = fields.Text(string='Route Notes')
    last_updated = fields.Datetime(string='Last Updated', default=fields.Datetime.now)

    @api.depends('departure_stop_id', 'arrival_stop_id')
    def _compute_distance(self):
        for route in self:
            if route.departure_stop_id and route.arrival_stop_id:
                # For now, set a default distance
                route.distance = 10.0
            else:
                route.distance = 0.0

    @api.depends('distance')
    def _compute_tariff(self):
        for route in self:
            # Base rate calculation
            base_rate = 5.55  # Base rate per km en dt
            # Calculate basic tariff
            route.tariff = route.distance * base_rate

    def calculate_tariff(self, include_holidays=False, without_holidays=False):
        self.ensure_one()
        base_tariff = self.tariff

        if without_holidays:
            base_tariff *= 1  
        
        # Add holiday surcharge if applicable
        if include_holidays:
            base_tariff *= 1.50  # surcharge for holidays

        return round(base_tariff, 2)

    @api.constrains('departure_stop_id', 'arrival_stop_id')
    def _check_stops(self):
        for route in self:
            if route.departure_stop_id == route.arrival_stop_id:
                raise ValidationError('Departure and arrival stops must be different')

    @api.model
    def create(self, vals):
        # Update last_updated timestamp on creation
        vals['last_updated'] = fields.Datetime.now()
        return super(Route, self).create(vals)

    def write(self, vals):
        # Update last_updated timestamp on write
        vals['last_updated'] = fields.Datetime.now()
        return super(Route, self).write(vals)