from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import date

class StudentStudent(models.Model):
    _name = 'student.student'

    name = fields.Char('Nombre')
    email = fields.Char("Correo Electronico")
    age = fields.Char("Edad", compute="_compute_age")
    birthdate = fields.Date('Fecha de nacimiento')
    gender = fields.Selection([('female', 'Femenino'), ('male','Masculino'), ('undefined', 'Sin definir')], string='Sexo/Género')
    phone = fields.Char('Numero de telefono')
    show_age = fields.Boolean('Mostrar edad', store=True)
    contract_ids = fields.One2many('contract.student', 'student_id', string='Contratos')
    career_id = fields.Many2one('career.career', string='Carrera a cursar')

    
    def check_age(self, age):
        if age < 17:
            raise ValidationError(_('El estudiante debe tener más de 17 años para poder ser registrado'))
        else:
            self.show_age = True 
        
    @api.depends('birthdate')
    def _compute_age(self):
        for record in self:
            if record.birthdate:
                today = date.today()
                born = fields.Date.from_string(record.birthdate)
                age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                record.age = age
                self.check_age(age)
            else:
                self.show_age = False
                record.age = ''
