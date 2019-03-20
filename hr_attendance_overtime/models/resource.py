# -*- coding: utf-8 -*-

import logging
from odoo import models, api

from odoo.addons.resource.models.resource import to_naive_user_tz

_logger = logging.getLogger(__name__)


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    def get_worked_within_after_hours(self, start_datetime, end_datetime, resource_id,
                                      min_tolerance_minutes=0):
        """
        Obtains the worked hours within and after the calendar for the related resource
        :param start_datetime:
        :param end_datetime:
        :param resource_id:
        :param min_tolerance_minutes:
        :return:
        """
        # TODO
        # * filter by public holidays
        # * use logger instead print

        # For an alternative calculation, see "_interval_remove_leaves" method

        work_intervals = []
        # The intervals are separated by days. For the current calculation,
        #  we prefer a single list
        _logger.info(
            'Within and after hours calculation for intervals between %s to %s, calendar_id=%d and resource_id=%d:'
            % (start_datetime, end_datetime, self.id, resource_id))
        i = 1
        for interval in self._iter_work_intervals(
                start_dt=start_datetime,
                end_dt=end_datetime,
                resource_id=resource_id):
            # data = [i]; data.extend(interval)
            k = 1
            for inter in interval:
                work_intervals.append(inter[0:2])
                _logger.info('%d.%d) from %s to %s' % (i, k, inter[0], inter[1]))
                k += 1
            i += 1

        # The current interval list does not take into account the public holidays
        # We're supress those intervals whose start datetime matches a public holiday day
        # UTC/TZ problem: datetime_from and datetime_and are expressed taking into account user TZ, because
        #  is_public_holiday uses attendance intervals un UTC.
        # E.g. with Europe/Madrid TZ, the public holiday 2019-03-19 (winter) actually starts
        #      in order to make comparisons with hr.attendance intervals we make check_in UTC date to user's TZ
        #      An attendance starting in 2019-03-18 23:30:00 UTC (or 2019-03-19 00:30:00 UTC+1) is converted to
        #      "2019-03-19 00:30:00 UTC" and is_public_holiday(), which compares only dates, is able to return True
        # As we said, We use the user TZ for this (manager users should be in the same TZ of the employees)
        employee_id = self.env['hr.employee'].search([('resource_id', '=', resource_id)]).id
        HolidaysPublic = self.env['hr.holidays.public']
        work_intervals = list(filter(
            lambda x: not HolidaysPublic.is_public_holiday(to_naive_user_tz(x[0], self.env.user),
                                                           employee_id=employee_id),
            work_intervals))

        worked_hours_within_calendar = worked_hours_after_calendar = 0

        # On every iteration, we compare the current work_interval with the last "initial" datetime registered
        #  (that will be the last "end" datetime or the attendance check in
        # Thus, the last iteration will confront the last "end" datetime for the work_interval (or the check in) with
        #  the check out
        dt_start = start_datetime
        min_tolerance_secs = 60 * min_tolerance_minutes
        for work_interval in work_intervals:
            work_dt_start = work_interval[0]
            work_dt_end = work_interval[1]
            offset_secs = (work_dt_start - dt_start).total_seconds()
            worked_hours_after_calendar += offset_secs / 3600 if offset_secs >= min_tolerance_secs else 0.0
            worked_hours_within_calendar += offset_secs / 3600 if offset_secs < min_tolerance_secs else 0.0
            worked_hours_within_calendar += (work_dt_end - work_dt_start).total_seconds() / 3600
            dt_start = work_dt_end
        if dt_start < end_datetime:
            # FIXME this will be the last (or unique) "empty" interval.
            #       But, if it isn't close to the next work interval and is lonely,
            #       should we always consider as after time?
            #       We don't know the work intervals outside (start_datetime, end_datetime)
            offset_secs = (end_datetime - dt_start).total_seconds()
            worked_hours_after_calendar += offset_secs / 3600 if offset_secs >= min_tolerance_secs else 0.0
            worked_hours_within_calendar += offset_secs / 3600 if offset_secs < min_tolerance_secs else 0.0

        """
        worked_hours_within_calendar = (end_datetime - start_datetime).total_seconds() / 3600
        worked_hours_after_calendar = 0
        """
        _logger.info('Obtained (%f, %f)' % (worked_hours_within_calendar, worked_hours_after_calendar))
        return worked_hours_within_calendar, worked_hours_after_calendar


class ResourceCalendarLeaves(models.Model):
    _inherit = 'resource.calendar.leaves'

    @api.model
    def create(self, values):
        leave_id = super(ResourceCalendarLeaves, self).create(values)
        self.env['hr.attendance'].worked_hours_within_after_recalculation(
            datetime_from=leave_id.date_from,
            datetime_to=leave_id.date_to,
            calendar_id=leave_id.calendar_id.id,
            resource_id=leave_id.resource_id.id)
        return leave_id

    def write(self, values):
        self.ensure_one()
        args_before = {
            'datetime_from': self.date_from,
            'datetime_to': self.date_to,
            'calendar_id': self.calendar_id.id,
            'resource_id': self.resource_id.id}
        ret = super(ResourceCalendarLeaves, self).write(values)
        if any(['date_from' in values, 'date_to' in values, 'resource_id' in values, 'calendar_id' in values]):
            args_after = {
                'datetime_from': values.get('datetime_from') or self.date_from,
                'datetime_to': values.get('datetime_to') or self.date_to,
                'calendar_id': values.get('calendar_id') or self.calendar_id.id,
                'resource_id': values.get('resource_id') or self.resource_id.id}
            self.env['hr.attendance'].worked_hours_within_after_recalculation(**args_before)
            self.env['hr.attendance'].worked_hours_within_after_recalculation(**args_after)
        return ret

    def unlink(self):
        for leave in self:
            args = {
                'datetime_from': leave.date_from,
                'datetime_to': leave.date_to,
                'calendar_id': leave.calendar_id.id,
                'resource_id': leave.resource_id.id}
            ret = super(ResourceCalendarLeaves, self).unlink()
            self.env['hr.attendance'].worked_hours_within_after_recalculation(**args)
            return ret

