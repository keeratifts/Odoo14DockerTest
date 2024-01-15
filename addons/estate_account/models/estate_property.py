from odoo import models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_button(self):
        '''
        Create empty invoice

        super(EstateProperty, self).sold_button()
        move_values = {
            'partner_id': self.buyer_id,
            'move_type': 'out_invoice'
        }
        move = self.env['account.move'].sudo().create(move_values)
        '''

        super(EstateProperty, self).sold_button()
        move_values = {
            'name': "Test",
            'partner_id': self.buyer_id,
            'move_type': 'out_invoice',
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "name": self.name,
                        "quantity": "1",
                        "price_unit": self.selling_price * 0.06,
                    },
                ),
                (
                    0,
                    0,
                    {
                        "name": "Administrative fees",
                        "quantity": "1",
                        "price_unit": 100,
                    },
                ),
            ]
        }
        
        move = self.env['account.move'].sudo().create(move_values)

        return move