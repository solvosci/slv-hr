# -*- coding: utf-8 -*-

from datetime import datetime, time

from odoo import api, fields, models


class HrHolidaysPublicLine(models.Model):
    _inherit = 'hr.holidays.public.line'

    @api.model
    def _check_worked_hours_within_after(self, date):
        """ Recomputes overtime hours affected by this public holiday """
        if isinstance(date, str):
            date = fields.Date.from_string(date)
        HrAttendance = self.env['hr.attendance']
        for calendar in self.env['resource.calendar'].search([]):
            # FIXME UTC / TZ problem
            HrAttendance.worked_hours_within_after_recalculation(
                datetime_from=fields.Datetime.to_string(datetime.combine(date, time(0, 0, 0))),
                datetime_to=fields.Datetime.to_string(datetime.combine(date, time(23, 59, 59, 99999))),
                calendar_id=calendar.id)

    @api.model
    def create(self, values):
        hpls = super(HrHolidaysPublicLine, self).create(values)
        for hpl in hpls:
            self._check_worked_hours_within_after(date=hpl.date)
        return hpls

    def write(self, values):
        # For simplicity we always force overtime recomputation (the state_ids should also be changed and
        #  it also affects even if date isn't changed)
        dates = set(self.mapped('date'))
        if 'date' in values:
            dates.add(values['date'])
        res = super(HrHolidaysPublicLine, self).write(values)
        for date in dates:
            self._check_worked_hours_within_after(date=date)
        return res

    def unlink(self):
        dates = set(self.mapped('date'))
        res = super(HrHolidaysPublicLine, self).unlink()
        for date in dates:
            self._check_worked_hours_within_after(date=date)
        return res

