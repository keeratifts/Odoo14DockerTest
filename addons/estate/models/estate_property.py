from odoo import api, fields, models
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
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
    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, default = lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', index=True, copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', "property_type_id", string="Offers")

    total_area = fields.Integer(compute="_compute_total_area", String="Total Area")

    # best_offer = fields.Float()
    best_offer = fields.Float(compute="_compute_display_best_offer", String="Best Offer")

    #specify dependecies
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self): #compute method is private so it should start with _
        for area in self:
            area.total_area = area.living_area + area.garden_area

    @api.depends("offer_ids.price")
    def _compute_display_best_offer(self):
        # print (self.offer_ids.mapped('price'))
        self.best_offer = max(self.offer_ids.mapped('price')) #list every record from this element

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = "10"
            self.garden_orientation = "north"
        else:
            self.garden_area = "0"
            self.garden_orientation = ""
