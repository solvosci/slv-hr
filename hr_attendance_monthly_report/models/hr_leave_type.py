# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, fields


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    type_hr_report = fields.Selection(
        [
            ("sick_leave", "Sick Leave"),
            ("day_off", "Day Off"),
            ("holidays", "Holidays"),
            ("public_holiday", "Public Holiday")
        ],
    )
