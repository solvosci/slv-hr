# -*- coding: utf-8 -*-

# Copyright 2019 Solvos Consultoría Informática, S.L.

{
    'name': 'Overtime additions to Theoretical vs Attended Time Analysis',
    'version': '0.1',
    'category': 'Human Resources',
    'website': 'https://github.com/solvosci/slv-hr',
    'author': 'Solvos Consultoría Informática',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'hr_attendance_report_theoretical_time',
        'hr_attendance_overtime',
    ],
    'data': [
        'reports/hr_attendance_theoretical_time_report_views.xml',
    ],
}
