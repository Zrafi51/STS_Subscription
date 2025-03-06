from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class STSFrontend(http.Controller):
    @http.route('/sts', type='http', auth='public', website=True)
    def homepage(self, **kwargs):
        return request.render('sts_front.homepage_template', {})

    @http.route('/sts/subscription', type='http', auth='user', website=True)
    def subscription_page(self, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                values = {
                    'subscription_type_1': kwargs.get('subscription_type'),
                    'subscription_type_2': 'special_tariff' if kwargs.get('include_holidays') else 'normal_tariff',
                    'route_ids': [(4, int(kwargs.get('route_id')))] if kwargs.get('route_id') else False,
                    'card_receiving_point': kwargs.get('receiving_point'),
                }
                
                # Create subscription
                subscription = request.env['sts_abon.abonnement'].sudo().create(values)
                
                # Create abonne record
                abonne_values = {
                    'name': request.env.user.name,
                    'date_of_birth': kwargs.get('date_of_birth'),
                    'user_type': request.env.user.user_type,
                    'institution': kwargs.get('institution'),
                    'university_id': kwargs.get('university_id'),
                    'school_id': kwargs.get('school_id'),
                    'parent_name': kwargs.get('parent_name'),
                    'cin': kwargs.get('cin'),
                }
                abonne = request.env['sts_abon.abonne'].sudo().create(abonne_values)
                
                return request.redirect(f'/sts/subscription/{subscription.id}')
            except Exception as e:
                routes = request.env['resroutier.route'].sudo().search([])
                return request.render('sts_front.subscription_template', {
                    'error': str(e),
                    'routes': routes
                })
                
        routes = request.env['resroutier.route'].sudo().search([])
        return request.render('sts_front.subscription_template', {
            'routes': routes
        })

    @http.route('/sts/subscription/<int:subscription_id>', type='http', auth='user', website=True)
    def view_subscription(self, subscription_id, **kwargs):
        subscription = request.env['sts_abon.abonnement'].sudo().browse(subscription_id)
        if not subscription.exists():
            return request.not_found()
        return request.render('sts_front.subscription_view_template', {
            'subscription': subscription,
        })
        
    @http.route('/sts/save-profile', type='http', auth='user', website=True, csrf=False)
    def save_profile(self, **kwargs):
        try:
            user = request.env.user
            vals = {
                'name': kwargs.get('name'),
                'date_of_birth': kwargs.get('date_of_birth'),
                'user_type': kwargs.get('user_type'),
                'cin': kwargs.get('cin'),
                'institution': kwargs.get('institution'),
                'university_id': kwargs.get('university_id'),
                'school_id': kwargs.get('school_id'),
                'parent_name': kwargs.get('parent_name'),
            }
            
            if 'profile_picture' in request.httprequest.files:
                vals['profile_picture'] = request.httprequest.files['profile_picture'].read()
            
            user.write(vals)
            return request.redirect('/sts/subscription')
        except Exception as e:
            return request.render('sts_front.Data_template', {
                'error': str(e)
            })