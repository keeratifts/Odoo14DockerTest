from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
    string='Status',
    selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    copy=False
    )
    partner_id = fields.Many2one('res.partner', string = "Buyer", required=True)
    property_id = fields.Many2one('estate.property', string = "Property", required = True)
    
    validity = fields.Integer(string = "Validity", default = "7")
    create_date = fields.Date(string = "Offer Date", copy=False, default=lambda self: datetime.now())
    date_deadline = fields.Date(string = "Offer Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _sql_contrasints = [
        ('positive_offer', 'CHECK(price >= 0)', 'An offer price must be strictly positive')
    ]
    
    @api.model
    def create(self, vals):
        # Retrieve the property record using property_id from vals
        property_id = self.env['estate.property'].browse(vals.get('property_id'))
        
        # Check if the new offer's price is lower than existing offers
        existing_offers = self.search([('property_id', '=', property_id.id)])
        if existing_offers and vals.get('price') <= max(existing_offers.mapped('price')):
            raise UserError(
                _(
                    "New offer cannot be lower that the existing one"
                )
            )

        return super(EstatePropertyOffer, self).create(vals)

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for date in self:
            if date.create_date:
                date.date_deadline = (date.create_date + timedelta(days=date.validity)).strftime('%Y-%m-%d')

    @api.depends("create_date")
    def _inverse_deadline(self):
        for date in self:
            if date.create_date:
                print ((date.date_deadline - date.create_date).days)
                date.validity = ((date.date_deadline - date.create_date).days)
    
    def accept_button(self):
        for record in self:
            if record.property_id.state == "new" or record.property_id.state == "offer":
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "accept"
                record.status = "accepted"
            else:
                msg = ("This property is not available")
                raise UserError(msg)

    
    def refuse_button(self):
        for record in self:
            if record.property_id.state == "new" or record.property_id.state == "offer":
                record.status = "refused"
            else:
                msg = ("This property is not available")
                raise UserError(msg)

