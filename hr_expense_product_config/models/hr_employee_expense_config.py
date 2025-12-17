# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo import _, fields, models


class HrEmployeeExpenseConfig(models.Model):
    _name = "hr.employee.expense.config"
    _description = "hr.employee.expense.config"

    product_id = fields.Many2one('product.product', domain=[('can_be_expensed', '=', True)])
    _sql_constraints = [('unique_product_per_employee',
        'unique (product_id, expense_employee_id, company_id)',
        _('No duplicate employee-product-company allowed.'))]
    expense_employee_id = fields.Many2one(comodel_name='hr.employee')
    payment_mode = fields.Selection(
        selection=[
            ('own_account', "Employee (to reimburse)"),
            ('company_account', "Company")
        ],
        string="Paid By",
    )
    has_expense_limit = fields.Boolean(string=("Has daily expense limit"))
    expense_limit_qty = fields.Monetary(string=("Daily expense limit amount"), currency_field='company_currency_id')
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company,
    )
    company_currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        readonly=True
    )
