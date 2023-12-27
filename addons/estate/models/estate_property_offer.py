from odoo import fields, models, api
from datetime import datetime, timedelta

class EstatePropertyTag(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
    string='Status',
    selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    copy=False
    )
    buyer_id = fields.Many2one('res.partner', string = "Buyer", required=True)
    property_type_id = fields.Many2one('estate.property', string = "Property", required=True)
    
    validity = fields.Integer(string = "Validity", default = "7")
    create_date = fields.Date(string = "Offer Date", copy=False, default=lambda self: datetime.now())
    date_deadline = fields.Date(string = "Offer Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

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

