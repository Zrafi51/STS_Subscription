from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

class AuthSignupHomeExtended(AuthSignupHome):

    @http.route('/web/login', type='http', auth='public', website=True)
    def web_login(self, redirect=None, **kw):
        if request.httprequest.method == 'POST':
            login = kw.get('login')
            password = kw.get('password')
            user = request.env['res.users'].sudo().search([('phone', '=', login)], limit=1)
            if user and user._check_password(password):
                request.env.cr.commit()
                request.session.uid = user.id
                return http.redirect_with_hash(redirect or '/web')
        return request.render('auth_login_template', {})
