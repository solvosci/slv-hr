# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo import _, api, models,fields
from odoo.exceptions import ValidationError


class HrExpense(models.Model):
    _inherit = "hr.expense"

    payment_locked = fields.Boolean(compute="_compute_payment_locked")
    allowed_product_ids = fields.Many2many(
        'product.product',
        compute='_compute_allowed_product_ids'
    )

    @api.depends('employee_id', 'company_id')
    def _compute_allowed_product_ids(self):
        for record in self:
            config_ids = self.env['hr.employee.expense.config'].search([
                ('expense_employee_id', '=', record.employee_id.id),
                ('company_id', 'in', [record.company_id.id, False]),
            ])
            record.allowed_product_ids = config_ids.mapped('product_id')

    @api.depends('employee_id', 'product_id', 'company_id')
    def _compute_payment_locked(self):
        for expense in self:
            config = expense.employee_id.expense_config_ids.filtered(lambda d: d.product_id == expense.product_id and d.company_id in [expense.company_id, False])[:1]
            expense.payment_locked = bool(config and config.payment_mode)

    @api.onchange('product_id')
    def _onchange_employee_config(self):
        config = self.employee_id.expense_config_ids.filtered(lambda d: d.product_id == self.product_id and d.company_id in (self.company_id, False))[:1]
        if config and config.payment_mode:
            self.payment_mode = config.payment_mode

    @api.constrains('total_amount_currency')
    def _check_daily_expense_limit(self):
        for expense in self:
            config = expense.employee_id.expense_config_ids.filtered(lambda d: d.product_id == expense.product_id and d.has_expense_limit and d.company_id in [expense.company_id, False])[:1]
            if config:
                same_expense_days = self.env['hr.expense'].search([
                    ("date", "=", expense.date),
                    ("product_id", "=", expense.product_id.id),
                    ("employee_id", "=", expense.employee_id.id),
                    ("company_id", "=", expense.company_id.id),
                ])
                total = sum([day.total_amount_currency for day in same_expense_days])
                if total > config.expense_limit_qty:
                    raise ValidationError(_('The total amount exceeds the limit per product per day'))
