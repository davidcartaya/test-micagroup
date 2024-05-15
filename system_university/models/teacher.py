from odoo import _, api, fields, models

class TeacherTeacher(models.Model):
    _name = 'teacher.teacher'

    name = fields.Char('Nombre')
    matter_id = fields.Many2one('matter.matter', string='Materia')