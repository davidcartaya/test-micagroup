# -*- coding: utf-8 -*-
{
    "name": "System",
    'version': '1.0',
    'summary': 'Gestión de materias y carreras',
    'description': 'Módulo para gestionar materias y carreras universitarias',    
    "author": "David Cartaya <david.cartaya2003@gmail.com>",
    "depends": ['base', 'web'],
    "data": [
        # archivos de seguridad
        'security/ir.model.access.csv',

        #archivo de secuencia
        'data/sequence_contract.xml',
        #archivo para cargar las monedas
        'data/currency_data.xml',
        #archivo para cargar las materias
        'data/matter_data.xml',
        #archivo para cargar las carreras
        'data/career_data.xml',
        #archivo para cargar los profesores
        'data/teacher_data.xml',
        #archivo para cargar los estudiantes
        'data/student_data.xml',

        # wizard para registrar pago de contrato
        'wizard/pay_contract.xml',

        # vistas
        'views/menu_items.xml',
        'views/currency_view.xml',
        'views/contract_view.xml',
        'views/student_view.xml',
        'views/matter_view.xml',
        'views/teacher_view.xml',
        'views/payment_contract_view.xml',
        'views/career.xml',
        'views/dashboard.xml',

    ],
    'installable': True,
}
