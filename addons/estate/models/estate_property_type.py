from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")

    _sql_contrasints = [
        ('unique_name', 'UNIQUE(name)', 'A property tag name and property type name must be unique')
    ]
