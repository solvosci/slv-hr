# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    def get_worked_within_after_hours(self, start_dt, end_dt, resource_id,
                                      min_tolerance_minutes=0):
        """
        Obtains the worked hours within and after the calendar for the related resource
        :param start_dt:
        :param end_dt:
        :param resource_id:
        :param min_tolerance_minutes:
        :return:
        """
        # TODO develop real code:
        # * get work intervals with _iter_work_intervals()
        # * filter by public holidays
        # * combine with (start_dt, end_dt) interval in order to extract hours
        #   (see "_interval_remove_leaves" method)
        # * after hours min tolerance correction
        worked_hours_within_calendar = \
            (fields.Datetime.from_string(end_dt) -
             fields.Datetime.from_string(start_dt)).total_seconds() / 3600
        worked_hours_after_calendar = 0
        return worked_hours_within_calendar, worked_hours_after_calendar
