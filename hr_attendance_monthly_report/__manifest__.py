# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "HR Attendace Monthly Report",
    "summary": """
        Adds new monthly attendance report per employee
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "14.0.1.0.3",
    "category": "Operations/HR",
    "website": "https://github.com/solvosci/slv-hr",
    "depends": [
        "hr_employee_ssn",
        "hr_holidays",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/hr_attendance_report.xml",
        "reports/hr_attendance_template.xml",
        "views/hr_leave_type_views.xml",
        "views/hr_menu.xml",
        "views/res_company_views.xml",
        "wizards/hr_attendance_wizard_views.xml",
    ],
    "installable": True,
}
