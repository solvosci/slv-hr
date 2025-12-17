# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo import _, fields, models


class HrEmployee(models.AbstractModel):
    _inherit = "hr.employee.base"

    expense_config_ids = fields.One2many(comodel_name='hr.employee.expense.config', inverse_name='expense_employee_id')
