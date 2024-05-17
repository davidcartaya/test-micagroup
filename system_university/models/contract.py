from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ContractStudent(models.Model):
    _name = 'contract.student'

    name = fields.Char('Número de contrato')
    student_id = fields.Many2one('student.student', string='Estudiante')
    contract_lines_ids = fields.One2many('contract.student.line', 'contract_id', string='Lineas de contrato')
    total_cost = fields.Float('Costo total', compute='_compute_total_cost', store=True)
    total_cost_usd = fields.Float('Costo total en USD', compute='_compute_total_cost_usd', store=True)
    state = fields.Selection([
            ('draft', 'Borrador'),
            ('confirm', 'Confirmado'),
            ('paid', 'Pagado'),
            ('cancel', 'Cancelado'),
            ('paid_cancel', 'Pago cancelado'),
        ], string='Estado', required=True, readonly=True, copy=False, tracking=True, default='draft')
    payment_id = fields.Many2one('payment.contract', string='Pago asociado')
    career_student_id = fields.Many2one('career.career', related='student_id.career_id', string='Carrera del estudiante', readonly=True, store=True)

    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == _("New") or vals['name'] == False:
            vals['name'] = self.env['ir.sequence'].next_by_code('contract.student')
        
        contract = super(ContractStudent, self).create(vals)
        
        if contract.career_student_id:
            new_lines = []
            for matter in contract.career_student_id.matter_ids:
                new_line = (0, 0, {
                    'matter_id': matter.id,
                    'contract_id': contract.id,
                })
                new_lines.append(new_line)
            contract.contract_lines_ids = new_lines
        
        if contract.student_id:
            contract.student_id.contract_ids |= contract
        
        return contract

    def write(self, vals):
        res = super(ContractStudent, self).write(vals)
        if 'student_id' in vals:
            self._update_contract_lines()
        return res

    def _update_contract_lines(self):
        self.ensure_one()
        self.contract_lines_ids = [(5, 0, 0)]
        new_lines = []
        for matter in self.career_student_id.matter_ids:
            new_line = (0, 0, {
                'matter_id': matter.id,
                'contract_id': self.id,
            })
            new_lines.append(new_line)
        self.contract_lines_ids = new_lines
    
    @api.onchange('career_student_id')
    def _onchange_lines(self):
        if self.career_student_id:
            self.contract_lines_ids = [(5, 0, 0)]
            new_lines = []
            for matter in self.career_student_id.matter_ids:
                new_line = (0, 0, {
                    'matter_id': matter.id,
                })
                new_lines.append(new_line)
            self.contract_lines_ids = new_lines

    
    @api.depends('contract_lines_ids')
    def _compute_total_cost(self):
        for contract in self:
            if contract.contract_lines_ids:
                contract.total_cost = sum(line.matter_cost for line in contract.contract_lines_ids if line.matter_cost)
            else:
                contract.total_cost = 0.0

    @api.depends('total_cost')
    def _compute_total_cost_usd(self):
        for record in self:
            usd_currency = self.env['custom.currency'].search([('code', '=', 'USD')], limit=1)

            if usd_currency:
                record.total_cost_usd = record.total_cost / usd_currency.rate
            else:
                record.total_cost_usd = 0

    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_confirm(self):
        for record in self:
            if record.contract_lines_ids:
                record.state = 'confirm'
            else:
                raise ValidationError(_("No puede confirmar un contrato sin lineas."))
    
    def action_cancel(self):
        for record in self:
            record.state = 'cancel'

    def action_post(self):
        for record in self: 
            record.state = 'paid'

class ContractStudentLine(models.Model):
    _name = 'contract.student.line'

    contract_id = fields.Many2one('contract.student', string='Contrato', readonly=True)
    matter_id = fields.Many2one('matter.matter', string='Materia')
    career_student_id = fields.Many2one(related='contract_id.career_student_id', string='Carrera del Estudiante')
    teacher_id = fields.Many2one('teacher.teacher', related='matter_id.teacher_id', string='Profesor asignado', store=True, readonly=True)
    matter_cost = fields.Float('Costo', related='matter_id.matter_cost', store=True, readonly=True)
    matter_cost_usd = fields.Float('Costo USD', related='matter_id.matter_cost_usd', store=True, readonly=True)
