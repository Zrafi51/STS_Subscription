from odoo import models, fields

class Abonne(models.Model):
    _name = 'sts_abon.abonne'
    _description = 'Abonnement de la STS'

    user_id = fields.Many2one('sts_abon.user', string='User', required=True)
    name = fields.Char(string='Full Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    user_type = fields.Selection([('intern', 'Intern'), ('student', 'Student'), ('schoolboy', 'Schoolboy')], string='User Type', required=True)
    institution = fields.Char(string='Institution')
    university_id = fields.Char(string='University ID')
    school_id = fields.Char(string='School ID')
    parent_name = fields.Char(string='Parent Name')
    cin = fields.Char(string='CIN', required=True)
    profile_picture = fields.Binary(string='Profile Picture')
    sql_constraints = [
        ('cin_unique', 'unique(cin)', 'CIN must be unique')
    ]
     #payment_status = fields.Selection([
     #    ('pending', 'En attente'),
     #    ('paid', 'Payé'),
     #    ('failed', 'Échec'),
     #], string='Statut de paiement', default='pending')