from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name, id"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1) #manually sorting

    _sql_contrasints = [
        ('unique_name', 'UNIQUE(name)', 'A property tag name and property type name must be unique')
    ]
