# -*- coding: utf-8 -*-

# Copyright 2019 Solvos Consultoría Informática, S.L.

{
    'name': 'HR attendance: allow own attendances read access for users',
    'version': '0.1',
    'category': 'Human Resources',
    'website': 'https://github.com/solvosci/slv-hr',
    'author': 'Solvos Consultoría Informática',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'hr_attendance',
    ],
    'data': [
        'security/hr_attendance_security.xml',
        'views/hr_attendance_views.xml',
    ],
}
