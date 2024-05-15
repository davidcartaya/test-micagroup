from odoo import models, fields, api

class Currency(models.Model):
    _name = 'custom.currency'

    name = fields.Char(string='Moneda', required=True)
    code = fields.Char(string='Codigo', required=True)
    rate = fields.Float(string='Tasa', required=True)
    symbol = fields.Char(string='Símbolo', required=True)
