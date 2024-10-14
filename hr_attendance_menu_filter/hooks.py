# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api


def uninstall_hook(env):
    env.ref("hr_attendance.hr_attendance_action").write(
        {
            "context": str({"search_default_employee": 1}),
        }
    )
    env.ref("hr_attendance.hr_attendance_reporting").write(
        {
            "context": str({
                "search_default_groupby_name" : 1,
                "search_default_employee": 1,
                "search_default_last_three_months": 1,
            }),
        }
    )
