from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")

    _sql_contrasints = [
        ('unique_name', 'UNIQUE(name)', 'A property tag name and property type name must be unique')
    ]
