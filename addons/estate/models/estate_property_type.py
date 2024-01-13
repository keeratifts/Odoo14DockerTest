from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name, id"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1) #manually sorting

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_count_offer", string="Amount of offer")

    _sql_contrasints = [
        ('unique_name', 'UNIQUE(name)', 'A property tag name and property type name must be unique')
    ]

    
    @api.depends("offer_ids")
    def _compute_count_offer(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
