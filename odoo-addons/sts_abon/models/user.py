from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
import hashlib
import secrets
from datetime import datetime, timedelta

class User(models.Model):
    _name = 'sts_abon.user'
    #_inherit = 'res.users'
    _description = 'Authentication and User Management'
    
    name = fields.Char(string='Name', required=True)
    surname = fields.Char(string='Surname', required=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)
    phone = fields.Char(string='Phone', required=True, unique=True)
    password_hash = fields.Char(string='Password Hash', required=True)
    salt = fields.Char(string='Password Salt', required=True)
    user_type = fields.Selection([
        ('student', 'Student'),
        ('intern', 'Intern'),
        ('schoolboy', 'Schoolboy')
    ], string='User Type', required=True)
    
    @api.depends('name', 'surname')
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.name} {record.surname}"

    # Verification
    verification_code = fields.Char(string='Verification Code')
    verification_expiry = fields.Datetime(string='Verification Code Expiry')
    is_verified = fields.Boolean(string='Is Verified', default=False)
    
    # Session management
    session_token = fields.Char(string='Session Token')
    session_expiry = fields.Datetime(string='Session Expiry')
    
    _sql_constraints = [
        ('phone_unique', 'unique(phone)', 'Phone number must be unique'),
    ]

    @api.constrains('phone')
    def _check_phone(self):
        tunisian_pattern = r'^(?:\+216)?(2[0-9]|3[0-9]|4[0-9]|5[0-9]|7[0-9]|9[0-9])\d{6}$'
        for record in self:
            if record.phone and not re.match(tunisian_pattern, record.phone):
                raise ValidationError("Invalid Tunisian phone number format. Example: +216 XX XXX XXX or XX XXX XXX")

    @api.model
    def generate_salt(self):
        return secrets.token_hex(16)

    @api.model
    def hash_password(self, password, salt):
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

    @api.model
    def create(self, vals):
        if 'password' in vals:
            salt = self.generate_salt()
            vals['salt'] = salt
            vals['password_hash'] = self.hash_password(vals['password'], salt)
            del vals['password']
        return super(User, self).create(vals)

    def write(self, vals):
        if 'password' in vals:
            salt = self.generate_salt()
            vals['salt'] = salt
            vals['password_hash'] = self.hash_password(vals['password'], salt)
            del vals['password']
        return super(User, self).write(vals)

    def verify_password(self, password):
        self.ensure_one()
        return self.password_hash == self.hash_password(password, self.salt)

    def generate_verification_code(self):
        code = ''.join(secrets.choice('0123456789') for _ in range(6))
        expiry = fields.Datetime.now() + timedelta(minutes=10)
        self.write({
            'verification_code': code,
            'verification_expiry': expiry
        })
        return code

    def verify_code(self, code):
        self.ensure_one()
        if not self.verification_code or not self.verification_expiry:
            return False
        if fields.Datetime.now() > self.verification_expiry:
            return False
        if self.verification_code != code:
            return False
        
        self.write({
            'is_verified': True,
            'verification_code': False,
            'verification_expiry': False
        })
        return True

    def generate_session(self):
        token = secrets.token_hex(32)
        expiry = fields.Datetime.now() + timedelta(days=7)
        self.write({
            'session_token': token,
            'session_expiry': expiry
        })
        return token

    def validate_session(self, token):
        self.ensure_one()
        if not self.session_token or not self.session_expiry:
            return False
        if self.session_token != token:
            return False
        if fields.Datetime.now() > self.session_expiry:
            return False
        return True