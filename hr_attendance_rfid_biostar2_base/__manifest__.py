# -*- coding: utf-8 -*-
{
    'name': "HR attendance for Biostar2 RFID base addon",
    'version': '0.1',
    'category': 'Human Resources',
    'website': 'https://github.com/solvosci/slv-hr',
    'author': 'Solvos Consultoría Informática',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base_external_dbsource_mysql',
        'hr_attendance_rfid',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'data/base_external_dbsource.xml',
        'views/res_config_settings_views.xml',
    ],
}