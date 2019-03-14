# -*- coding: utf-8 -*-

# Copyright 2019 Solvos Consultoría Informática, S.L.

{
    'name': 'HR attendance overtime',
    'version': '0.1',
    'category': 'Human Resources',
    'website': 'https://github.com/solvosci/slv-hr',
    'author': 'Solvos Consultoría Informática',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'hr_attendance',
        'hr_holidays',
        'hr_holidays_public',
    ],
    'data': [
        # 'security/hr_attendance_rfid.xml',
        # 'security/ir.model.access.csv',
        'views/hr_attendance_views.xml',
        'views/res_config_settings_views.xml',
        # 'report/report_views.xml',
        # 'report/report_menuitem.xml',
    ],
}
