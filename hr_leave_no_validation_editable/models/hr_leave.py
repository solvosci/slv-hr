# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields,_
from odoo.exceptions import ValidationError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    def action_update_hr_leave_wizard(self):
        if self.env.user != self.employee_id.user_id or self.holiday_status_id.leave_validation_type != 'no_validation' or self.request_date_from <= fields.Date.today() or self.request_unit_half:
            raise ValidationError(_("Only your own leave that do not require validation before today can be edited."))
        wizard_id = self.env['hr.leave.edit.data.wizard'].sudo().create({
            'hr_leave_id': self.id,
            'request_date_from': self.request_date_from,
            'request_date_to': self.request_date_to,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'request_unit_hours': self.request_unit_hours,
            'request_unit_half': self.request_unit_half,
            'request_hour_from': self.request_hour_from,
            'request_hour_to': self.request_hour_to,
            'name': self.name,
        })
        return {
            'name': _('Update Hr Leave'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.leave.edit.data.wizard',
            'res_id': wizard_id.id,
            'target': 'new',
        }
