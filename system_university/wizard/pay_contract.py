from odoo import models, fields, api
from odoo.exceptions import UserError

class PayContractWizard(models.TransientModel):
    _name = 'pay.contract.wizard'

    amount = fields.Float(string='Monto del contrato')
    contract_id = fields.Many2one('contract.student', string='Contrato')
    amount_pay = fields.Float(string='Monto a pagar', related="amount", readonly=False)
    amount_pay_usd = fields.Float('Monto a pagar en USD', compute='_compute_amount_pay_usd')

    @api.depends('amount_pay')
    def _compute_amount_pay_usd(self):
        for wizard in self:
            usd_currency = self.env['custom.currency'].search([('code', '=', 'USD')], limit=1)

            if usd_currency:
                wizard.amount_pay_usd = wizard.amount_pay / usd_currency.rate
            else:
                wizard.amount_pay_usd = 0

    @api.model
    def default_get(self, fields):
        res = super(PayContractWizard, self).default_get(fields)
        if self.env.context.get('active_id') and self.env.context.get('active_model') == 'contract.student':
            contract = self.env['contract.student'].browse(self.env.context.get('active_id'))
            if contract:
                res.update({'amount': contract.total_cost})
                res.update({'contract_id': contract.id})
        return res

    def pay_contract(self):
        payment_obj = self.env['payment.contract']
        
        for record in self:
            if not record.amount_pay:
                raise UserError('Por favor ingrese un monto a pagar.')

            payment_vals = {
                'name': 'Pago para ' + record.contract_id.name,
                'amount': record.amount_pay,
                'contract_id': record.contract_id.id,
                'payment_date': fields.Date.today()
            }
            payment = payment_obj.create(payment_vals)

            record.contract_id.payment_id = payment.id

            record.contract_id.state = 'paid'
