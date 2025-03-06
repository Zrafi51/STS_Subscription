import requests
from odoo import models, fields

class UniversityApi(models.Model):
    _name = 'api_services.university_api'
    _description = 'University API Service'

    def get_university_data(self, university_id):
        try:
            # Replace with actual API endpoint
            api_url = "https://api.university.tn/v1/students"
            headers = {
                "Authorization": "Bearer YOUR_API_KEY",
                "Content-Type": "application/json"
            }
            response = requests.get(f"{api_url}/{university_id}", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}