from odoo import http
from odoo.http import request

class AuthSignupHomeExtended(http.Controller):

    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_signup(self, **kw):
        if request.httprequest.method == 'POST':
            name = kw.get('name')
            phone = kw.get('phone')
            password = kw.get('password')
            if name and phone and password:
                user = request.env['res.users'].sudo().create({
                    'name': name,
                    'login': phone,
                    'phone': phone,
                    'password': password,
                })
                request.env.cr.commit()
                request.session.uid = user.id
                return http.redirect_with_hash('/web')
        return request.render('auth_signup_template', {})
