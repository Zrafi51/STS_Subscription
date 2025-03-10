import vonage
from odoo import models

class SmsApi(models.Model):
    _name = 'api_services.sms_api'
    _description = 'SMS API Service'
    
    def send_sms(self, phone, message):
        try:
            client = vonage.Client(key="bff207d6", secret="j1JNJE13ns3O77Re")
            sms = vonage.Sms(client)
            
            response = sms.send_message({
                "from": "STS",
                "to": phone,
                "text": message,
            })

            if response["messages"][0]["status"] == "0":
                return True
            else:
                return False
        except Exception as e:
            return False