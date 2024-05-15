from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class MatterMatter(models.Model):
    _name = 'matter.matter'

    name = fields.Char('Nombre')
    teacher_id = fields.Many2one('teacher.teacher', string='Profesor asignado')
    matter_cost = fields.Float('Costo')
    matter_cost_usd = fields.Float('Costo USD', compute="_compute_matter_cost_usd")
    code = fields.Char('Código')
    career_id = fields.Many2one('career.career', string='Carrera')

    @api.onchange('teacher_id')
    def _onchange_teacher_id(self):
        if self.teacher_id and self.teacher_id.matter_id:
            return {
                'warning': {
                    'title': _('Advertencia'),
                    'message': _('Este profesor ya está asignado a otra materia.'),
                },
                'value': {'teacher_id': False}
            }

        available_teachers = self.env['teacher.teacher'].search([('matter_id', '=', False)])
        return {'domain': {'teacher_id': [('id', 'in', available_teachers.ids)]}}
    
    @api.model
    def create(self, vals):
        record = super(MatterMatter, self).create(vals)
        if record.teacher_id:
            record.teacher_id.write({'matter_id': record.id})
        if record.career_id:
            record.career_id.write({'matter_ids': [(4, record.id)]})
        return record

    def write(self, vals):
        if 'teacher_id' in vals:
            new_teacher_id = vals.get('teacher_id')
            current_teacher = self.teacher_id

            if current_teacher and current_teacher.id != new_teacher_id:
                current_teacher.matter_id = False

            new_teacher = self.env['teacher.teacher'].browse(new_teacher_id)

            if new_teacher:
                new_teacher.matter_id = self.id
        
        return super(MatterMatter, self).write(vals)
    

    @api.depends('matter_cost')
    def _compute_matter_cost_usd(self):
        for record in self:
            usd_currency = self.env['custom.currency'].search([('code', '=', 'USD')], limit=1)

            if usd_currency:
                record.matter_cost_usd = record.matter_cost / usd_currency.rate
            else:
                record.matter_cost_usd = 0
    

