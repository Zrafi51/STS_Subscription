import requests
from odoo import models, fields

class CinApi(models.Model):
    _name = 'api_services.cin_api'
    _description = 'CIN API Service'

    def get_user_data_by_cin(self, cin):
        try:
            # Replace with actual API endpoint
            api_url = "https://api.cin.tn/v1/citizens"
            headers = {
                "Authorization": "Bearer YOUR_API_KEY",
                "Content-Type": "application/json"
            }
            response = requests.get(f"{api_url}/{cin}", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}