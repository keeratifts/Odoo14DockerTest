from odoo import fields, models
from datetime import datetime, timedelta

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
