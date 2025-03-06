from odoo import models, fields, api

class Stop(models.Model):
    _name = 'resroutier.stop'
    _description = 'Bus Stop'

    name = fields.Char(string='Stop Name', required=True)
    location = fields.Char(string='Location', required=True)
    coordinates = fields.Char(string='GPS Coordinates')

    # Relations
    departure_route_ids = fields.One2many('resroutier.route', 'departure_stop_id', string='Departure Routes')
    arrival_route_ids = fields.One2many('resroutier.route', 'arrival_stop_id', string='Arrival Routes')
    
    # Additional fields
    description = fields.Text(string='Description')