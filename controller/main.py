from odoo import http
import json

class RealEstateController(http.Controller):

    @http.route('/real_estate/records', auth='public', website=True)
    def get_real_estate_records(self, **kw):
        # Logic to retrieve real estate records from your model
        real_estate_records = http.request.env['real_state.real'].sudo().search([])


        response = {
            'records': real_estate_records,
        }

        # Return a template with the records
        return http.request.render('real_estate.template_real_estate_records', response)

class RealEstateControllerApi(http.Controller):

    @http.route('/api/real_estate/records', auth='public', type='json', website=True)
    def get_real_estate_records(self, **kwargs):
        real_estate_records = http.request.env['real_state.real'].sudo().search([])
        records_data = [
            {'name': record.name, 'bedrooms': record.bedrooms, 'garage': record.garage, 'garden': record.garden} for
            record in real_estate_records]
        json_data = json.dumps(records_data)
        return json.loads(json_data)