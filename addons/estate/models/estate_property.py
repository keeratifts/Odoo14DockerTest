from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
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
    living_area = fields.Integer(string="Living Area (sqm)", default = "0")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)", default = "0")
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
    offer_ids = fields.One2many('estate.property.offer', "property_id", string="Offers")

    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")

    # best_offer = fields.Float()
    best_offer = fields.Float(compute="_compute_display_best_offer", string="Best Offer", default="0")

    _sql_contrasints = [
        ('positive_expected_price', 'CHECK(expected_price >= 0)', 'A property expected price must be strictly positive'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'A property selling price must be positive')
    ]
    #specify dependecies
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self): #compute method is private so it should start with _
        for area in self:
            area.total_area = area.living_area + area.garden_area

    @api.depends("offer_ids.price")
    def _compute_display_best_offer(self):
        for record in self:
            if record.offer_ids.mapped('price') != []:
                record.best_offer = max(record.offer_ids.mapped('price')) #list every record
            else:
                record.best_offer = "0"

    
    # @api.depends("state")
    # def _compute_offer_state(self):
    #     for record in self:
    #         if len(record.offer_ids.mapped('price')) >= 1:
    #             record.state = "offer"
    #         else:
    #             record.state = "new"

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = "10"
            self.garden_orientation = "north"
        else:
            self.garden_area = "0"
            self.garden_orientation = ""
    
    @api.constrains('selling_price')
    def selling_price_not_less_than_90(self):
        for record in self:
            if record.selling_price > 0:
                if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) <= 0:
                    raise ValidationError("Selling price cannot be lower than 90 of the expected price.")

    def sold_button(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
                return True
            else:
                msg = ("This property cannot be sold")
                raise UserError(msg)
    
    def cancel_button(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
                return True
            else:
                msg = ("This property cannot be canceled")
                raise UserError(msg)