# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo import _,api, fields, models
from odoo.exceptions import ValidationError


class HrContract(models.Model):
    _inherit = "hr.contract"

    tax_total_pct = fields.Float(
        string="Personal Income Tax"
    )

    @api.constrains('tax_total_pct')
    def _check_tax_total_pct(self):
        for employee in self:
            if not (0 <= employee.tax_total_pct <= 1):
                raise ValidationError(_("The tax must be between 0 and 100. The tax of %(employee)s is %(tax)s%%", employee=employee.employee_id.name, tax=employee.tax_total_pct * 100))
