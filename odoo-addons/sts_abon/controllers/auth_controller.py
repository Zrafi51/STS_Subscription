from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class AuthController(http.Controller):

    @http.route('/auth/signup', type='http', auth='public', website=True, csrf=False)
    def signup(self, **kwargs):
        """Handles signup with phone number authentication."""
        if request.httprequest.method == 'POST':
            try:
                required_fields = ['name', 'phone', 'password']
                missing = [f for f in required_fields if not kwargs.get(f)]
                if missing:
                    return request.render('sts_abon.signup_template', {'error': f"Missing fields: {', '.join(missing)}"})

                # Create user
                user = request.env['res.users'].sudo().create({
                    'name': kwargs['name'],
                    'phone': kwargs['phone'],
                    'login': kwargs['phone'],  # Login will be phone number
                    'password': kwargs['password'],
                })

                # Generate and send OTP
                otp = user.generate_otp()
                sms_api = request.env['api_services.sms_api'].sudo()
                sms_api.send_sms(user.phone, f"Your STS verification code is: {otp}")

                return request.redirect(f'/auth/verify?user_id={user.id}')
            except Exception as e:
                _logger.error(f"Error during signup: {str(e)}")
                return request.render('sts_abon.signup_template', {'error': str(e)})

        return request.render('sts_abon.signup_template', {})

    @http.route('/auth/verify', type='http', auth='public', website=True, csrf=False)
    def verify_phone(self, **kwargs):
        """Handles phone verification via OTP."""
        user_id = kwargs.get('user_id')
        if request.httprequest.method == 'POST':
            try:
                user = request.env['res.users'].sudo().browse(int(user_id))
                if user.verify_otp(kwargs.get('verification_code')):
                    return request.redirect('/auth/login')
                else:
                    return request.render('sts_abon.verification_template', {'user_id': user.id, 'error': 'Invalid verification code'})
            except Exception as e:
                _logger.error(f"Error during verification: {str(e)}")
                return request.render('sts_abon.verification_template', {'user_id': user_id, 'error': str(e)})
        return request.render('sts_abon.verification_template', {'user_id': user_id})

    @http.route('/auth/login', type='http', auth='public', website=True, csrf=False)
    def login(self, **kwargs):
        """Handles login with phone number."""
        if request.httprequest.method == 'POST':
            try:
                user = request.env['res.users'].sudo().search([('phone', '=', kwargs.get('phone'))], limit=1)

                if not user or not user._check_password(kwargs.get('password')):
                    return request.render('sts_abon.login_template', {'error': 'Invalid credentials'})

                if not user.phone_verified:
                    return request.render('sts_abon.login_template', {'error': 'Phone number not verified', 'requires_verification': True, 'user_id': user.id})

                request.session.uid = user.id
                return request.redirect('/sts/subscription')
            except Exception as e:
                _logger.error(f"Error during login: {str(e)}")
                return request.render('sts_abon.login_template', {'error': str(e)})

        return request.render('sts_abon.login_template', {})
