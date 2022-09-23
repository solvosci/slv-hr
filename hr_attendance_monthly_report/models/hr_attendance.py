# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields


class HrAttendance(models.Model):
    _inherit ='hr.attendance'

    def action_hr_attendance_monthly_report(self):
        Wizard = self.env['hr.attendance.wizard']
        new = Wizard.create({
            'month_year': fields.Datetime().now()
        })
        return {
            'name': 'Custom report',
            'res_model': 'hr.attendance.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': new.id,
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
