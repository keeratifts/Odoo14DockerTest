from odoo import fields, models

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
    
