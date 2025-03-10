from odoo import models, fields, api
from datetime import datetime

class Abonnement(models.Model):
    _name = 'sts_abon.abonnement'
    _description = 'STS Subscription Management'

    creation_date = fields.Date(default=fields.Date.today)

    subscription_type_1 = fields.Selection([
        ('semester', 'First Semester (15/09 - 15/12)'),
        ('annual', 'Annual (15/09 - 30/06)')
    ], compute='_compute_subscription_type_1', store=True)

    @api.depends('creation_date')
    def _compute_subscription_type_1(self):
        for record in self:
            if record.creation_date:
                creation_date_obj = fields.Date.from_string(record.creation_date)
                if creation_date_obj.month > 6:
                    record.subscription_type_1 = 'semester'
                else:
                    record.subscription_type_1 = 'annual'

    start_date = fields.Date(compute='_compute_start_date', store=True)
    end_date = fields.Date(compute='_compute_end_date', store=True)

    subscription_type_2 = fields.Selection([
        ('normal_tariff', 'without holidays'),
        ('special_tariff', 'include holidays')
    ], required=True)

    #route_ids --> choix route(depart, arrivé, tariff)
    route_ids = fields.Many2many('resroutier.route', required=True)
    card_receiving_point =fields.Char(string='Card Receiving Point', required=True)
    
    # payment_status = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('paid', 'Paid'),
    #     ('expired', 'Expired')
    # ], default='draft')

    @api.depends('creation_date')
    def _compute_start_date(self):
        for record in self:
            if record.creation_date:
                creation_date_obj = fields.Date.from_string(record.creation_date)
                if creation_date_obj.month < 6:
                    record.start_date = datetime(creation_date_obj.year - 1, 9, 15).date()
                else:
                    record.start_date = datetime(creation_date_obj.year, 9, 15).date()

    @api.depends('subscription_type_1', 'creation_date')
    def _compute_end_date(self):
        for record in self:
            if record.creation_date:
                creation_date_obj = fields.Date.from_string(record.creation_date)
                if record.subscription_type_1 == 'semester':
                    record.end_date = datetime(creation_date_obj.year - 1, 12, 15).date()
                else:  # Annual subscription
                    if creation_date_obj.month < 6:
                        record.end_date = datetime(creation_date_obj.year, 6, 30).date()
                    else:
                        record.end_date = datetime(creation_date_obj.year + 1, 6, 30).date()
    # def action_confirm_payment(self):
    #     self.write({'payment_status': 'paid'})
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'reload'
    #     }