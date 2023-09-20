# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrLeave(models.Model):
    _inherit = "hr.leave"

    manager_user_id = fields.Many2one(
        comodel_name="res.users",
        compute="_compute_manager_user_id",
        string="Manager",
        store=True,
        help="""
        User that is allowed to approve/validate/refuse employee's leaves
        """,
    )

    @api.depends("employee_id", "employee_id.parent_id")
    def _compute_manager_user_id(self):
        for holiday in self:
            holiday.manager_user_id = (
                holiday.employee_id.parent_id
                and holiday.employee_id.parent_id.user_id
                or holiday.employee_id.user_id
            )

    def action_approve(self):
        for holiday in self:
            holiday._check_security_manager_rights()
        super().action_approve()

    def action_validate(self):
        for holiday in self:
            holiday._check_security_manager_rights()
        super().action_validate()

    def action_refuse(self):
        for holiday in self:
            holiday._check_security_manager_rights()
        super().action_refuse()

    def _check_security_manager_rights(self):
        self.ensure_one()
        if (
            self.manager_user_id.id != self.env.user.id
            and
            not self.env.user.has_group(
                "hr_holidays.group_hr_holidays_manager"
            )
        ):
            err_msg = ""
            if self.manager_user_id:
                err_msg = _(
                    "Only %s or a Leave Manager can approve/validate/refuse"
                    " leaves for the employee %s"
                ) % (self.manager_user_id.name, self.employee_id.name)
            else:
                err_msg = _(
                    "Only a Leave Manager can approve/validate/refuse"
                    " leaves for the employee %s"
                ) % self.employee_id.name
            raise UserError(err_msg)
