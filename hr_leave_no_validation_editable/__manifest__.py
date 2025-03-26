# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)
{
    "name": "Hr Leave No Validation Editable",
    "summary": """
        Adds button to be able to edit your own leaves that do not require validation before the end date.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "13.0.1.0.0",
    "category": "Human Resources",
    "website": "https://github.com/solvosci/slv-hr",
    "depends": ['hr_holidays'],
    "data": [
        "views/hr_leave_views.xml",
        "wizards/hr_leave_edit_data_wizard_views.xml",
    ],
    'installable': True,
}
