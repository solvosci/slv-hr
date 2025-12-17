# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Hr Expense Product Configuration",
    "summary": """
        Allows setting expense configurations per employee, company, and product combination.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Human Resources",
    "website": "https://github.com/solvosci/slv-hr",
    "depends": [
        "hr_expense"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/hr_employee_views.xml",
        "views/hr_expense_views.xml"
    ],
    "installable": True,
}
