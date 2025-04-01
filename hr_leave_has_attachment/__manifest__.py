# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Hr Leave Has Attachment",
    "summary": """
        Adds new field to hr.leave model to check if there are any attachments.
    """,
    "author": "Solvos",
    "license": "AGPL-3",
    "version": "13.0.1.0.1",
    "category": "Human Resources",
    "website": "https://github.com/solvosci/slv-hr",
    "depends": ['hr_holidays'],
    "data": [
        "views/hr_leave_views.xml",
    ],
    'installable': True,
    'pre_init_hook': 'pre_init_hook'
}
