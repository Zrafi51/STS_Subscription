from odoo import http
from odoo.http import request

class PaymentController(http.Controller):

    @http.route('/payment/callback', type='http', auth='public', csrf=False)
    def payment_callback(self, **kwargs):
        """
        Callback endpoint for payment confirmation.
        """
        transaction_id = kwargs.get('transaction_id')
        if not transaction_id:
            return "Invalid request", 400

        payment = request.env['sts_abon.payment_transaction'].sudo().search([('transaction_id', '=', transaction_id)], limit=1)
        if not payment:
            return "Transaction not found", 404

        if payment.confirm_payment(transaction_id):
            return "Payment confirmed", 200
        else:
            return "Payment failed", 400