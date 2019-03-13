# -*- coding: utf-8 -*-

import logging
from odoo import models

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
