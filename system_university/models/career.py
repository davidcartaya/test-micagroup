from odoo import models, fields, api, _

class CareerCareer(models.Model):
    _name = 'career.career'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código')
    matter_ids = fields.Many2many('matter.matter', string='Materias')

    @api.model
    def create(self, vals):
        record = super(CareerCareer, self).create(vals)
        if 'matter_ids' in vals:
            for matter in record.matter_ids:
                matter.career_id = record.id
        return record

    def write(self, vals):
        if 'matter_ids' in vals:
            current_matters = self.matter_ids
            new_matters = self.env['matter.matter'].browse(vals.get('matter_ids')[0][2])
            for matter in current_matters - new_matters:
                matter.career_id = False
            for matter in new_matters - current_matters:
                matter.career_id = self.id
        return super(CareerCareer, self).write(vals)