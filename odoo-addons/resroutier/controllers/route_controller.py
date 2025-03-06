from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class RouteController(http.Controller):

    @http.route('/api/states', type='json', auth='public', methods=['GET'])
    def get_states(self):
        try:
            _logger.info("Fetching states from the database...")
            # Fetch unique states from the route model
            routes = request.env['resroutier.route'].sudo().search([])
            states = list(set(route.state_name for route in routes if route.state_name))
            _logger.info("States fetched: %s", states)
            return {"states": states}  # Return a JSON object with a "states" key
        except Exception as e:
            _logger.error("Error fetching states: %s", str(e))
            return {"error": str(e)}

    @http.route('/api/sides', type='json', auth='public', methods=['GET'])
    def get_sides(self, state):
        try:
            _logger.info("Fetching sides for state: %s", state)
            # Fetch unique sides for the selected state
            routes = request.env['resroutier.route'].sudo().search([('state_name', '=', state)])
            sides = list(set(route.side_name for route in routes if route.side_name))
            _logger.info("Sides fetched: %s", sides)
            return {"sides": sides}  # Return a JSON object with a "sides" key
        except Exception as e:
            _logger.error("Error fetching sides: %s", str(e))
            return {"error": str(e)}

    @http.route('/api/routes', type='json', auth='public', methods=['GET'])
    def get_routes(self):
        try:
            _logger.info("Fetching routes from the database...")
            routes = request.env['resroutier.route'].sudo().search([])
            result = [{
                'id': route.id,
                'state_name': route.state_name,
                'side_name': route.side_name,
                'route_name': route.route_name,
                'departure': route.departure_stop_id.name,
                'arrival': route.arrival_stop_id.name,
                'tariff': route.tariff,
                'centre_exploitation': route.centre_exploitation
            } for route in routes]
            _logger.info("Routes fetched: %s", result)
            return {"routes": result}  # Return a JSON object with a "routes" key
        except Exception as e:
            _logger.error("Error fetching routes: %s", str(e))
            return {"error": str(e)}

    @http.route('/api/stops', type='json', auth='public', methods=['GET'])
    def get_stops(self):
        """
        Fetch all stops from the resroutier.stop model.
        Returns a JSON object with a "stops" key containing the list of stops.
        """
        try:
            _logger.info("Fetching stops from the database...")
            stops = request.env['resroutier.stop'].sudo().search([])
            result = [{
                'id': stop.id,
                'name': stop.name,
                'location': stop.location
            } for stop in stops]
            _logger.info("Stops fetched: %s", result)
            return {"stops": result}  # Return a JSON object with a "stops" key
        except Exception as e:
            _logger.error("Error fetching stops: %s", str(e))
            return {"error": str(e)}

    @http.route('/api/route/tariff', type='json', auth='public', methods=['GET'])
    def get_route_tariff(self, departure_stop_id, arrival_stop_id):
        try:
            _logger.info("Fetching tariff for route: %s -> %s", departure_stop_id, arrival_stop_id)
            route = request.env['resroutier.route'].sudo().search([
                ('departure_stop_id', '=', int(departure_stop_id)),
                ('arrival_stop_id', '=', int(arrival_stop_id))
            ], limit=1)

            if not route:
                _logger.warning("Route not found: %s -> %s", departure_stop_id, arrival_stop_id)
                return {"error": "Route not found"}

            result = {
                'tariff': route.calculate_tariff(),
                'state_name': route.state_name,
                'side_name': route.side_name,
                'route_name': route.route_name,
                'distance': route.distance
            }
            _logger.info("Tariff fetched: %s", result)
            return result
        except Exception as e:
            _logger.error("Error fetching tariff: %s", str(e))
            return {"error": str(e)}