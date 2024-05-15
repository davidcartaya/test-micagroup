from odoo import models, fields, api

class Payment(models.Model):
    _name = 'payment.contract'

    name = fields.Char(string='Nombre', required=True)
    amount = fields.Float(string='Monto', required=True)
    payment_date = fields.Date(string='Fecha de Pago', default=fields.Date.today())
    contract_id = fields.Many2one('contract.student', string='Contrato relacionado')

    state = fields.Selection([
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', default='confirmed', readonly=True)

    def action_cancel(self):
        for record in self:
            record.contract_id.state = "paid_cancel"
            record.state = 'cancelled'