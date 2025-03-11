from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class AuthController(http.Controller):


    @http.route('/sts/save-profile', type='http', auth='user', website=True)
    def create_profile(self, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                user = request.env.user
                abonne_values = {
                    'user_id': user.id,  # Link the profile to the current user
                    'name': kwargs.get('name'),
                    'date_of_birth': kwargs.get('date_of_birth'),
                    'user_type': kwargs.get('user_type'),
                    'institution': kwargs.get('institution'),
                    'university_id': kwargs.get('university_id'),
                    'school_id': kwargs.get('school_id'),
                    'parent_name': kwargs.get('parent_name'),
                    'cin': kwargs.get('cin'),
                }
                abonne = request.env['sts_abon.abonne'].sudo().create(abonne_values)
                return request.redirect('/sts/subscription')
            except Exception as e:
                return request.render('sts_abon.data_template', {'error': str(e)})
        return request.render('sts_abon.data_template', {})

    @http.route('/auth/signup', type='http', auth='public', website=True, csrf=False)
    def signup(self, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                # Validate required fields
                required_fields = ['name', 'surname', 'phone', 'password']
                missing = [f for f in required_fields if not kwargs.get(f)]
                if missing:
                    return request.render('sts_abon.signup_template', {
                        'error': f"Missing required fields: {', '.join(missing)}"
                    })

                # Create user
                user = request.env['sts_abon.user'].sudo().create({
                    'name': kwargs['name'],
                    'surname': kwargs['surname'],
                    'phone': kwargs['phone'],
                    'password': kwargs['password'],
                    'user_type': kwargs.get('user_type', 'student')
                })

                # Generate and send verification code
                verification_code = user.generate_verification_code()
                sms_api = request.env['api_services.sms_api'].sudo()
                sms_api.send_sms(
                    user.phone,
                    f"Your STS verification code is: {verification_code}"
                )

                return request.redirect(f'/auth/verify?user_id={user.id}')
            
            except Exception as e:
                _logger.error(f"Error during signup: {str(e)}")
                return request.render('sts_abon.signup_template', {
                    'error': str(e)
                })

        return request.render('sts_abon.signup_template', {})

    @http.route('/auth/verify', type='http', auth='public', website=True, csrf=False)
    def verify_page(self, **kwargs):
        user_id = kwargs.get('user_id')
        if request.httprequest.method == 'POST':
            try:
                user = request.env['sts_abon.user'].sudo().browse(int(user_id))
                if user.verify_code(kwargs.get('verification_code')):
                    return request.redirect('/auth/login')
                else:
                    return request.render('sts_abon.verification_template', {
                        'user_id': user.id,
                        'error': 'Invalid verification code'
                    })
            except Exception as e:
                _logger.error(f"Error during verification: {str(e)}")
                return request.render('sts_abon.verification_template', {
                    'user_id': user_id,
                    'error': str(e)
                })
        return request.render('sts_abon.verification_template', {
            'user_id': user_id,
        })

    @http.route('/auth/login', type='http', auth='public', website=True, csrf=False)
    def login(self, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                user = request.env['sts_abon.user'].sudo().search([('phone', '=', kwargs.get('phone'))], limit=1)
                
                if not user or not user.verify_password(kwargs.get('password')):
                    return request.render('sts_abon.login_template', {
                        'error': 'Invalid credentials'
                    })

                if not user.is_verified:
                    return request.render('sts_abon.login_template', {
                        'error': 'Account not verified',
                        'requires_verification': True,
                        'user_id': user.id
                    })

                # Generate session token
                session_token = user.generate_session()
                request.session.uid = user.id
                return request.redirect('/sts/subscription')
            except Exception as e:
                _logger.error(f"Error during login: {str(e)}")
                return request.render('sts_abon.login_template', {
                    'error': str(e)
                })
        return request.render('sts_abon.login_template', {})

    @http.route('/auth/forgot-password', type='http', auth='public', website=True, csrf=False)
    def forgot_password(self, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                phone = kwargs.get('phone')
                user = request.env['sts_abon.user'].sudo().search([('phone', '=', phone)], limit=1)
                if not user:
                    return request.render('sts_abon.forgot_password_template', {
                        'error': 'User not found'
                    })
            
                # Generate and send verification code
                verification_code = user.generate_verification_code()
                sms_api = request.env['api_services.sms_api'].sudo()
                sms_api.send_sms(
                    user.phone,
                    f"Your STS password recovery code is: {verification_code}"
                )
            
                return request.redirect(f'/auth/reset-password?user_id={user.id}')
            except Exception as e:
                _logger.error(f"Error during forgot password: {str(e)}")
                return request.render('sts_abon.forgot_password_template', {
                    'error': str(e)
                })
        return request.render('sts_abon.forgot_password_template', {})