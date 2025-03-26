# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)
from odoo import models, fields, api, _
from datetime import datetime, time
from pytz import timezone, UTC
from odoo.addons.resource.models.resource import float_to_time
import math
import pytz

class HrLeaveEditDataWizard(models.TransientModel):
    _name = 'hr.leave.edit.data.wizard'
    _description = 'hr.leave.edit.data.wizard'

    name = fields.Char(string='Description')

    hr_leave_id = fields.Many2one('hr.leave', string='Leave')
    holiday_status_id = fields.Many2one(related='hr_leave_id.holiday_status_id')

    date_from = fields.Datetime(string='Start Date')
    date_to = fields.Datetime(string='End Date')
    request_date_from = fields.Date('Start Date')
    request_date_to = fields.Date('End Date')

    tz = fields.Selection(related='hr_leave_id.tz')

    request_unit_custom = fields.Boolean()
    request_unit_hours = fields.Boolean()
    request_unit_half = fields.Boolean()
    request_hour_from = fields.Selection([
        ('0', '0:00 AM'), ('0.5', '0:30 AM'),
        ('1', '1:00 AM'), ('1.5', '1:30 AM'),
        ('2', '2:00 AM'), ('2.5', '2:30 AM'),
        ('3', '3:00 AM'), ('3.5', '3:30 AM'),
        ('4', '4:00 AM'), ('4.5', '4:30 AM'),
        ('5', '5:00 AM'), ('5.5', '5:30 AM'),
        ('6', '6:00 AM'), ('6.5', '6:30 AM'),
        ('7', '7:00 AM'), ('7.5', '7:30 AM'),
        ('8', '8:00 AM'), ('8.5', '8:30 AM'),
        ('9', '9:00 AM'), ('9.5', '9:30 AM'),
        ('10', '10:00 AM'), ('10.5', '10:30 AM'),
        ('11', '11:00 AM'), ('11.5', '11:30 AM'),
        ('12', '12:00 PM'), ('12.5', '12:30 PM'),
        ('13', '1:00 PM'), ('13.5', '1:30 PM'),
        ('14', '2:00 PM'), ('14.5', '2:30 PM'),
        ('15', '3:00 PM'), ('15.5', '3:30 PM'),
        ('16', '4:00 PM'), ('16.5', '4:30 PM'),
        ('17', '5:00 PM'), ('17.5', '5:30 PM'),
        ('18', '6:00 PM'), ('18.5', '6:30 PM'),
        ('19', '7:00 PM'), ('19.5', '7:30 PM'),
        ('20', '8:00 PM'), ('20.5', '8:30 PM'),
        ('21', '9:00 PM'), ('21.5', '9:30 PM'),
        ('22', '10:00 PM'), ('22.5', '10:30 PM'),
        ('23', '11:00 PM'), ('23.5', '11:30 PM')], string='Hour from')
    request_hour_to = fields.Selection([
        ('0', '0:00 AM'), ('0.5', '0:30 AM'),
        ('1', '1:00 AM'), ('1.5', '1:30 AM'),
        ('2', '2:00 AM'), ('2.5', '2:30 AM'),
        ('3', '3:00 AM'), ('3.5', '3:30 AM'),
        ('4', '4:00 AM'), ('4.5', '4:30 AM'),
        ('5', '5:00 AM'), ('5.5', '5:30 AM'),
        ('6', '6:00 AM'), ('6.5', '6:30 AM'),
        ('7', '7:00 AM'), ('7.5', '7:30 AM'),
        ('8', '8:00 AM'), ('8.5', '8:30 AM'),
        ('9', '9:00 AM'), ('9.5', '9:30 AM'),
        ('10', '10:00 AM'), ('10.5', '10:30 AM'),
        ('11', '11:00 AM'), ('11.5', '11:30 AM'),
        ('12', '12:00 PM'), ('12.5', '12:30 PM'),
        ('13', '1:00 PM'), ('13.5', '1:30 PM'),
        ('14', '2:00 PM'), ('14.5', '2:30 PM'),
        ('15', '3:00 PM'), ('15.5', '3:30 PM'),
        ('16', '4:00 PM'), ('16.5', '4:30 PM'),
        ('17', '5:00 PM'), ('17.5', '5:30 PM'),
        ('18', '6:00 PM'), ('18.5', '6:30 PM'),
        ('19', '7:00 PM'), ('19.5', '7:30 PM'),
        ('20', '8:00 PM'), ('20.5', '8:30 PM'),
        ('21', '9:00 PM'), ('21.5', '9:30 PM'),
        ('22', '10:00 PM'), ('22.5', '10:30 PM'),
        ('23', '11:00 PM'), ('23.5', '11:30 PM')], string='Hour end')

    @api.onchange('request_hour_from', 'request_hour_to', 'request_date_from', 'request_date_to')
    def _onchange_request_parameters(self):
        if not self.request_date_from:
            self.date_from = False
            return

        compensated_request_date_from = self.request_date_from
        compensated_request_date_to = self.request_date_to
        hour_from = self.date_from.time()
        hour_to = self.date_to.time()
        date_from = datetime.combine(compensated_request_date_from, hour_from)
        date_to = datetime.combine(compensated_request_date_to, hour_to)

        if self.request_unit_hours:
            hour_from = float_to_time(float(self.request_hour_from))
            hour_to = float_to_time(float(self.request_hour_to))
            self.request_date_to = self.request_date_from
            date_from = timezone(self.tz).localize(datetime.combine(compensated_request_date_from, hour_from)).astimezone(UTC).replace(tzinfo=None)
            date_to = timezone(self.tz).localize(datetime.combine(compensated_request_date_to, hour_to)).astimezone(UTC).replace(tzinfo=None)

        self.update({'date_from': date_from, 'date_to': date_to})

    def action_edit_data(self):
        data = {
            'request_date_from': self.request_date_from,
            'request_date_to': self.request_date_to,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'name': self.name,
        }
        if self.request_unit_hours :
            data.update({
                'request_unit_hours': True,
                'request_hour_from': self.request_hour_from,
                'request_hour_to': self.request_hour_to,
            })

        if not self.request_unit_hours:
            employee = self.hr_leave_id.employee_id
            calendar = employee.resource_calendar_id

            if calendar:
                weekday_from = self.date_from.weekday()
                weekday_to = self.date_to.weekday()

                attendance_from = calendar.attendance_ids.filtered(
                    lambda a: int(a.dayofweek) == weekday_from
                )
                attendance_to = calendar.attendance_ids.filtered(
                    lambda a: int(a.dayofweek) == weekday_to
                )
                if attendance_from and attendance_to:
                    hour_from = min(attendance_from.mapped('hour_from'))
                    time_from = time(int(hour_from), int(round((hour_from % 1) * 60)))
                    hour_to = max(attendance_to.mapped('hour_to'))
                    time_to = time(int(hour_to), int(round((hour_to % 1) * 60)))

                    new_date_from = timezone(self.tz).localize(datetime.combine(self.date_from, time_from)).astimezone(UTC).replace(tzinfo=None)
                    new_date_to = timezone(self.tz).localize(datetime.combine(self.date_to, time_to)).astimezone(UTC).replace(tzinfo=None)

                    data.update({
                        'date_from': new_date_from,
                        'date_to': new_date_to,
                    })
        self.hr_leave_id.sudo().action_refuse()
        self.hr_leave_id.sudo().action_draft()
        self.hr_leave_id.sudo().write(data)
        self.hr_leave_id.sudo()._onchange_leave_dates()
        self.hr_leave_id.sudo()._compute_number_of_hours_display()
        self.hr_leave_id.sudo()._compute_duration_display()
        self.hr_leave_id.sudo().action_confirm()

        return {'type': 'ir.actions.act_window_close'}
