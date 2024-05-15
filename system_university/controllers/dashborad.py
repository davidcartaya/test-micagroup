from odoo import models, fields
from odoo import http
from odoo.http import request
import requests


class PowerBIController(http.Controller):

    @http.route('/powerbi/dashboard', type='http', auth='user', website=True)
    def render_dashboard(self, **kwargs):
        powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiN2UyZDUzZTUtMTZmMi00YjMwLWFlZTEtZTk2NzQ1NjJhZ[%E2%80%A6]6IjBiMTgwYjAyLTIzMTUtNDBjMS05ZWIxLTY0MDk4N2FmNDRkYyIsImMiOjl9"
        return request.render('system_university.powerbi_dashboard_template', {'powerbi_url': powerbi_url})