from odoo import http
from odoo.http import request
import json
from werkzeug.exceptions import BadRequest, Unauthorized

class AuthController(http.Controller):

    def _validate_required_fields(self, data, fields):
        missing = [f for f in fields if not data.get(f)]
        if missing:
            raise BadRequest(f"Missing required fields: {', '.join(missing)}")

    @http.route('/auth/signup', type='http', auth='public', methods=['GET', 'POST'], website=True, csrf=False)
    def signup(self, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                required_fields = ['name', 'surname', 'phone', 'password']
                self._validate_required_fields(kwargs, required_fields)
            
                user = request.env['auth.user'].sudo().create({
                    'name': kwargs['name'],
                    'surname': kwargs['surname'],
                    'phone': kwargs['phone'],
                    'password': kwargs['password'],
                    'user_type': kwargs.get('user_type', 'student')
                })

                verification_code = user.generate_verification_code()
            
                # Send SMS verification
                sms_api = request.env['api_services.sms_api'].sudo()
                sms_api.send_sms(
                    user.phone,
                    f"Your STS verification code is: {verification_code}"
                )

                return request.redirect(f'/auth/verify?user_id={user.id}')
            
            except Exception as e:
                return request.render('sts_front.signup_template', {
                    'error': str(e)
                })
        return request.render('sts_front.signup_template', {})

    @http.route('/auth/verify', type='http', auth='public', website=True, csrf=False)
    def verify_page(self, **kwargs):
        user_id = kwargs.get('user_id')
        if request.httprequest.method == 'POST':
            try:
                user = request.env['auth.user'].sudo().browse(int(user_id))
                if user.verify_code(kwargs.get('verification_code')):
                    return request.redirect('/sts/login')
                else:
                    return request.render('sts_front.verification_template', {
                        'user_id': user.id,
                        'error': 'Invalid verification code'
                    })
            except Exception as e:
                return request.render('sts_front.verification_template', {
                    'user_id': user_id,
                    'error': str(e)
                })
        return request.render('sts_front.verification_template', {
            'user_id': user_id,
        })
        
    @http.route('/auth/login', type='http', auth='public', website=True, csrf=False)
    def login(self, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                user = request.env['auth.user'].sudo().search([('phone', '=', kwargs.get('phone'))], limit=1)
                
                if not user or not user.verify_password(kwargs.get('password')):
                    return request.render('sts_front.login_template', {
                        'error': 'Invalid credentials'
                    })

                if not user.is_verified:
                    return request.render('sts_front.login_template', {
                        'error': 'Account not verified',
                        'requires_verification': True,
                        'user_id': user.id
                    })

                session_token = user.generate_session()
                request.session.uid = user.id
                return request.redirect('/sts/subscription')
            except Exception as e:
                return request.render('sts_front.login_template', {
                    'error': str(e)
                })
        return request.render('sts_front.login_template', {})

    @http.route('/auth/forgot-password', type='http', auth='public', website=True, csrf=False)
    def forgot_password(self, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                phone = kwargs.get('phone')
                user = request.env['auth.user'].sudo().search([('phone', '=', phone)], limit=1)
                if not user:
                    return request.render('sts_front.forgot_password_template', {
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
                return request.render('sts_front.forgot_password_template', {
                    'error': str(e)
                })
        return request.render('sts_front.forgot_password_template', {})

    @http.route('/auth/reset-password', type='http', auth='public', website=True, csrf=False)
    def reset_password(self, **kwargs):
        user_id = kwargs.get('user_id')
        if request.httprequest.method == 'POST':
            try:
                user = request.env['auth.user'].sudo().browse(int(user_id))
                if not user:
                    return request.render('sts_front.reset_password_template', {
                        'error': 'User not found',
                        'user_id': user_id
                    })
            
                if not user.verify_code(kwargs.get('code')):
                    return request.render('sts_front.reset_password_template', {
                        'error': 'Invalid verification code',
                        'user_id': user_id
                    })
            
                if kwargs.get('new_password') != kwargs.get('confirm_password'):
                    return request.render('sts_front.reset_password_template', {
                        'error': 'Passwords do not match',
                        'user_id': user_id
                    })
            
                # Update password
                user.write({
                    'password': kwargs.get('new_password')
                })
            
                return request.redirect('/auth/login')
            except Exception as e:
                return request.render('sts_front.reset_password_template', {
                    'error': str(e),
                    'user_id': user_id
                })
        return request.render('sts_front.reset_password_template', {
            'user_id': user_id
        })