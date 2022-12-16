# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Employee Leaves - Manager approval",
    "summary": """
    Only user that is the Employee Manager of a certain employee can approve,
    validate or refuese that employee leaves
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "11.0.1.1.0",
    "category": "Human Resources",
    "website": "https://github.com/solvosci/slv-hr",
    "depends": ["hr_holidays"],
    "data": ["views/hr_holidays_views.xml"],
    "installable": True,
}
