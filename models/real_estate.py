import datetime

from odoo import fields,models,api

class real(models.Model):
    _name="real_state.real"
    name=fields.Char()
    bedrooms=fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_orientation = fields.Selection([('east', 'East'), ('west', 'West'), ('north', 'North'), ('south', 'South')])
    area = fields.Float("Area")
    garden_area = fields.Float("Garden Area")
    total_area = fields.Float("Total Area")
    date_availability = fields.Date()
    remaining_days = fields.Integer("Remaining Days", compute="compute_remaining_days",readonly=True)
    partener_id=fields.Many2one(comodel_name="res.partner")
    tages_id=fields.Many2many('real.estate.tags')
    offer_id=fields.One2many("realestate.offers","real_estate_id","Offer Line")
    garden_orientation = fields.Selection([('east','East'),('west','West')])
    email=fields.Char()
    image_ids = fields.Many2many(
        'ir.attachment',
        string='Images',
        compute='_compute_image_ids',
        store=True,  # Store the computed value in the database
        copy=False,
    )

    def _compute_image_ids(self):
        for record in self:
            image_attachments = self.env['ir.attachment'].search([
                ('res_model', '=', 'your.model'),  # Adjust this to your model name
                ('res_id', '=', record.id),
                ('mimetype', 'like', 'image/%'),  # Filter by image MIME types
            ])
            record.image_ids = [(6, 0, image_attachments.ids)]
    _sql_constraints=[
        ("Unique_Name","UNIQUE(name)","This Name is exist"),
        ("Unique_email", "UNIQUE(email)", "This email is exist"),
    ]
    @api.onchange("area","garden_area")
    def totalCalc(self):
       if self.area >0 and self.garden_area >0:
          self.total_area=self.area+self.garden_area
       else:
           self.total_area=0

    @api.depends("date_availability")
    def compute_remaining_days(self):
        for record in self:
            if record.date_availability:
                remaining_days = (record.date_availability - datetime.date.today()).days
                record.remaining_days = remaining_days if remaining_days >= 0 else 0
            else:
                record.remaining_days = 0

class realOffers(models.Model):
    _name="realestate.offers"
    _rec_name="real_estate_id"
    real_estate_id = fields.Many2one("real_state.real")
    partner_id = fields.Many2one("res.partner", "Partner")
    desc = fields.Char("Desc")
    price = fields.Float("Price")
    offer_date = fields.Date("Offer Date")
class RealEstateTags(models.Model):
    _name = 'real.estate.tags'
    name = fields.Char("Name")