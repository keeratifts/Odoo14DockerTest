from odoo import fields, models

class InheritedUserModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'salesperson_id', string = 'Property', domain="[('date_availability', '&lt;=', datetime.datetime.now().strftime('%Y-%m-%d')), ('state', '=', 'new')]")
    # kk = fields.Char(string="kk")