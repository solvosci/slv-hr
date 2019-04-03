# -*- coding: utf-8 -*-
# Copyright 2019 Solvos Consultoría Informática, S.L.

{
    'name': 'HR attendance Check in/out from Biostar2 RFID database',
    'version': '0.1',
    'category': 'Human Resources',
    'website': 'https://github.com/solvosci/slv-hr',
    'author': 'Solvos Consultoría Informática',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'hr_attendance_rfid_biostar2_base',
    ],
    'data': [
        # 'security/hr_attendance_rfid.xml',
        # 'security/ir.model.access.csv',
        # 'views/hr_attendance.xml',
        # 'views/res_config_settings.xml',
        # 'report/report_views.xml',
        # 'report/report_menuitem.xml',
        'views/res_config_settings_views.xml'
    ],
    'demo': [
        # 'demo/'
    ]
}
