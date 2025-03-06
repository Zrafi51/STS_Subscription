from odoo import models, fields, api
import requests
import json

class PaymentTransaction(models.Model):
    _name = 'sts_abon.payment_transaction'
    _description = 'Payment Transactions'

    subscription_id = fields.Many2one('sts_abon.abonnement', string='Subscription', required=True)
    amount = fields.Float(string='Amount', required=True)
    transaction_id = fields.Char(string='Transaction ID')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ], string='Status', default='draft')
    payment_date = fields.Datetime(string='Payment Date')

    def initiate_payment(self):
        """
        Initiate payment via the payment gateway API.
        """
        self.ensure_one()
        api_url = "https://api.payment-gateway.tn/payment/create"  # Replace with the actual API endpoint
        headers = {
            "Authorization": "Bearer YOUR_API_KEY",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": self.amount,
            "currency": "TND",
            "description": f"Payment for subscription {self.subscription_id.id}",
            "callback_url": f"{request.httprequest.host_url}/payment/callback",  # Callback URL for payment confirmation
            "metadata": {
                "subscription_id": self.subscription_id.id,
            }
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            if result.get('success'):
                self.write({
                    'transaction_id': result.get('transaction_id'),
                    'status': 'pending',
                })
                return result.get('payment_url')  # Redirect user to this URL for payment
            else:
                self.write({'status': 'failed'})
                raise ValueError("Payment initiation failed: " + result.get('message', 'Unknown error'))
        except Exception as e:
            self.write({'status': 'failed'})
            raise ValueError(f"Payment initiation failed: {str(e)}")

    def confirm_payment(self, transaction_id):
        """
        Confirm payment via the payment gateway API.
        """
        self.ensure_one()
        api_url = f"https://api.payment-gateway.tn/payment/confirm/{transaction_id}"  # Replace with the actual API endpoint
        headers = {
            "Authorization": "Bearer YOUR_API_KEY",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            result = response.json()

            if result.get('status') == 'paid':
                self.write({
                    'status': 'paid',
                    'payment_date': fields.Datetime.now(),
                })
                return True
            else:
                self.write({'status': 'failed'})
                return False
        except Exception as e:
            self.write({'status': 'failed'})
            raise ValueError(f"Payment confirmation failed: {str(e)}")