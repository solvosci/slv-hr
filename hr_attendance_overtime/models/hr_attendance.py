# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    worked_hours_within_calendar = fields.Float(
        'Worked hours within calendar',
        compute='_compute_worked_hours_within_after_calendar')
    worked_hours_after_calendar = fields.Float(
        'Worked hours within calendar',
        compute='_compute_worked_hours_within_after_calendar')
    """
    resource_calendar_id = fields.Many2one(
        'Employee calendar',
        related='employee_id.resource_calendar_id',
        readonly=True)
    company_id = fields.Many2one(
        'Employee company',
        related='employee_id.company_id',
        readonly=True)
    """

    @api.depends('check_in', 'check_out')
    def _compute_worked_hours_within_after_calendar(self):
        """ Calculates two different categories for worked hours:
            * Worked within employee calendar
            * Worked after employee calendar
            There's a company parameter (after_calendar_min_tolerance_minutes) used for move calendar/overtime limits

            Example for some attendances (for a calendar 08:00-12:00 and 15 min tolerance):
            - 07:55-12:05 : worked=4h 10min ; within=4h 10min ; after=0h 00min
            - 08:05-12:05 : worked=4h 00min ; within=4h 00min ; after=0h 00min
            - 07:40-12:05 : worked=4h 25min ; within=4h 05min ; after=0h 20min

            Approved leaves and public holidays always implies computed after hours, ignoring calendar
        """
        ResourceCalendar = self.env['resource.calendar']
        for att in self:
            if att.check_in and att.check_out:
                att.worked_hours_within_calendar, att.worked_hours_after_calendar = \
                    ResourceCalendar.get_worked_within_after_hours(
                        att.check_in, att.check_out, att.employee_id.resource_id.id,
                        att.employee_id.company_id.after_calendar_min_tolerance_minutes
                    )
            else:
                att.worked_hours_within_calendar, att.worked_hours_after_calendar = (0, 0)
