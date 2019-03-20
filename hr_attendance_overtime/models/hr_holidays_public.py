# -*- coding: utf-8 -*-

from datetime import datetime, time

from odoo import api, fields, models

from odoo.addons.resource.models.resource import to_naive_utc


class HrHolidaysPublicLine(models.Model):
    _inherit = 'hr.holidays.public.line'

    @api.model
    def _check_worked_hours_within_after(self, date):
        """ Recomputes overtime hours affected by this public holiday """
        if isinstance(date, str):
            date = fields.Date.from_string(date)
        HrAttendance = self.env['hr.attendance']
        # UTC/TZ problem: datetime_from and datetime_and are expressed taking into account user tx, because
        #  worked_hours_within_after_recalculation uses attendance intervals un UTC.
        # E.g. with Europe/Madrid TZ, the public holiday 2019-03-19 (winter) actually starts
        #      at 2019-03-18 23:00:00 UTC and finishes at 2019-03-19 22:59:59.99999 UTC
        #      in order to make comparisons with hr.attendance intervals
        # We use the user TZ for this (manager users should be in the same TZ of the employees)
        datetime_from = fields.Datetime.to_string(
            to_naive_utc(datetime.combine(date, time(0, 0, 0)), self.env.user))
        datetime_to = fields.Datetime.to_string(
            to_naive_utc(datetime.combine(date, time(23, 59, 59, 99999)), self.env.user))
        for calendar in self.env['resource.calendar'].search([]):
            HrAttendance.worked_hours_within_after_recalculation(
                datetime_from=datetime_from,
                datetime_to=datetime_to,
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

