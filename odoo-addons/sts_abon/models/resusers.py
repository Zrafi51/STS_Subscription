from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    phone = fields.Char(related='partner_id.phone', store=True, readonly=False)
