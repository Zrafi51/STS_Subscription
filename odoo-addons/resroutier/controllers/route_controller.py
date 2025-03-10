from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class RouteController(http.Controller):

    @http.route('/api/routes', type='json', auth='public', methods=['GET'])
    def get_routes(self):
        try:
            _logger.info("Fetching routes from the database...")
            routes = request.env['resroutier.route'].sudo().search([])
            result = [{
                'id': route.id,
                'route_name': route.route_name,
                'departure': route.departure_stop_id.name,
                'arrival': route.arrival_stop_id.name,
                'tariff': route.tariff,
                'centre_exploitation': route.centre_exploitation
            } for route in routes]
            _logger.info("Routes fetched: %s", result)
            return {"routes": result}
        except Exception as e:
            _logger.error("Error fetching routes: %s", str(e))
            return {"error": str(e)}

    @http.route('/api/route/tariff', type='json', auth='public', methods=['GET'])
    def get_route_tariff(self, route_id):
        try:
            _logger.info("Fetching tariff for route: %s", route_id)
            route = request.env['resroutier.route'].sudo().browse(int(route_id))
            if not route:
                _logger.warning("Route not found: %s", route_id)
                return {"error": "Route not found"}
    
            result = {
                'tariff': route.calculate_tariff(),
                'route_name': route.route_name,
                'distance': route.distance,
                'receiving_points': [
                    {'id': point.id, 'name': point.name}
                    for point in route.centre_exploitation.split(',')
                ]
            }
            _logger.info("Tariff fetched: %s", result)
            return result
        except Exception as e:
            _logger.error("Error fetching tariff: %s", str(e))
            return {"error": str(e)}