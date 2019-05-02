
from odoo import api, fields, models, tools
from datetime import datetime, time
from psycopg2.extensions import AsIs
from dateutil import tz


class HrAttendanceTheoreticalTimeReport(models.Model):
    _inherit = "hr.attendance.theoretical.time.report"

    worked_hours_within_calendar = fields.Float(
        'Within',
        readonly=True)
    worked_hours_after_calendar = fields.Float(
        'After',
        readonly=True)


    def _select(self):
        # We put "max" aggregation function for theoretical hours because
        # we will recompute for other detail levels different than day
        # through recursivity by day results and will aggregate them manually
        return """
            %s,
            sum(worked_hours_within_calendar) AS worked_hours_within_calendar,
            sum(worked_hours_after_calendar) AS worked_hours_after_calendar 
            """ % super(HrAttendanceTheoreticalTimeReport, self)._select()
        return """
            min(id) AS id,
            employee_id,
            date,
            sum(worked_hours) AS worked_hours,
            max(theoretical_hours) AS theoretical_hours,
            sum(difference) AS difference
            """

    def _select_sub1(self):
        return """
            %s,
            ha.worked_hours_within_calendar AS worked_hours_within_calendar,
            ha.worked_hours_after_calendar AS worked_hours_after_calendar
            """ % super(HrAttendanceTheoreticalTimeReport, self)._select_sub1()

    def _select_sub2(self):
        return """
            %s,
            0.0 AS worked_hours_within_calendar,
            0.0 AS worked_hours_after_calendar
            """ % super(HrAttendanceTheoreticalTimeReport, self)._select_sub2()