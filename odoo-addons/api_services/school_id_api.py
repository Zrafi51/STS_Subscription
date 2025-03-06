import requests
from odoo import models, fields

class SchoolApi(models.Model):
    _name = 'api_services.school_api'
    _description = 'School API Service'

    def get_school_data(self, school_id):
        try:
            # Replace with actual API endpoint
            api_url = "https://api.education.tn/v1/schools"
            headers = {
                "Authorization": "Bearer YOUR_API_KEY",
                "Content-Type": "application/json"
            }
            response = requests.get(f"{api_url}/{school_id}", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}