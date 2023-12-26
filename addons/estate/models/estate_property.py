from odoo import fields, models
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    property_type_id = fields.Char()
    # property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=lambda self: (datetime.now() + timedelta(days=3*30)).strftime('%Y-%m-%d'))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')]
    )
    active = fields.Boolean(string='Active', default=True, help='Set to False to deactivate this record')
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer', 'Offer Received'), ('accept', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        copy = False,
        default = 'new'
    )