from odoo import http
from odoo.http import request
import json
from werkzeug.exceptions import BadRequest

class SubscriptionController(http.Controller):


    @http.route('/sts/subscription', type='http', auth='user', website=True)
    def subscription_page(self, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                user = request.env.user
                abonne_id = int(kwargs.get('abonne_id'))  # Get the selected profile ID
                abonne = request.env['sts_abon.abonne'].sudo().browse(abonne_id)

                values = {
                    'abonne_id': abonne.id,  # Link the subscription to the selected profile
                    'subscription_type_1': kwargs.get('subscription_period'),
                    'subscription_type_2': 'special_tariff' if kwargs.get('include_holidays') == 'true' else 'normal_tariff',
                    'route_ids': [(4, int(kwargs.get('route_id')))] if kwargs.get('route_id') else False,
                }
                subscription = request.env['sts_abon.abonnement'].sudo().create(values)
                return request.redirect(f'/sts/subscription/{subscription.id}')
            except Exception as e:
                routes = request.env['resroutier.route'].sudo().search([])
                abonnes = request.env['sts_abon.abonne'].sudo().search([('user_id', '=', request.env.user.id)])
                return request.render('sts_abon.subscription_template', {
                    'error': str(e),
                    'routes': routes,
                    'abonnes': abonnes,  # Pass the list of profiles to the template
                })
        
        routes = request.env['resroutier.route'].sudo().search([])
        abonnes = request.env['sts_abon.abonne'].sudo().search([('user_id', '=', request.env.user.id)])
        return request.render('sts_abon.subscription_template', {
            'routes': routes,
            'abonnes': abonnes,  # Pass the list of profiles to the template
        })
    
    @http.route('/api/subscription/create', type='json', auth='public', methods=['POST'])
    def create_subscription(self, **kwargs):
        try:
            # Validate user type and get appropriate API
            user_type = kwargs.get('user_type')
            if user_type == 'student' or user_type == 'intern':
                api = request.env['api_services.university_api'].sudo()
                api_data = api.get_university_data(kwargs.get('university_id'))
            elif user_type == 'schoolboy':
                api = request.env['api_services.school_api'].sudo()
                api_data = api.get_school_data(kwargs.get('school_id'))
            
            # Validate CIN
            cin_api = request.env['api_services.cin_api'].sudo()
            cin_data = cin_api.get_user_data_by_cin(kwargs.get('cin'))
            
            if cin_data.get('error'):
                return {'error': 'Invalid CIN'}

            # Create subscription
            vals = {
                'name': kwargs.get('name'),
                'date_of_birth': kwargs.get('date_of_birth'),
                'user_type': user_type,
                'cin': kwargs.get('cin'),
                'institution': api_data.get('institution'),
                'university_id': kwargs.get('university_id') if user_type in ['student', 'intern'] else False,
                'school_id': kwargs.get('school_id') if user_type == 'schoolboy' else False,
                'parent_name': kwargs.get('parent_name') if user_type == 'schoolboy' else False,
            }
            
            subscription = request.env['sts_abon.abonne'].sudo().create(vals)
            return {'success': True, 'subscription_id': subscription.id}
            
        except Exception as e:
            return {'error': str(e)}