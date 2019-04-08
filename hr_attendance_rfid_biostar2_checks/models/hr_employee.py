# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, exceptions, _
_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def attendance_action_change(self, action_date=None):
        """ ATTENTION!!! Overrides odoo/hr_attendance/hr_employee.py/attendance_action_change original method in order tho add
                the action_date parameter. By default (action date is now) the original bevavior is guaranteed

            Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        if len(self) > 1:
            raise exceptions.UserError(_('Cannot perform check in or check out on multiple employees.'))
        # ---------------------------------------------------------------------
        # original code:
        #  action_date = fields.Datetime.now()
        if not action_date:
            action_date = fields.Datetime.now()
        # ---------------------------------------------------------------------

        if self.attendance_state != 'checked_in':
            vals = {
                'employee_id': self.id,
                'check_in': action_date,
            }
            return self.env['hr.attendance'].create(vals)
        else:
            attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
            if attendance:
                attendance.check_out = action_date
            else:
                raise exceptions.UserError(_('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                    'Your attendances have probably been modified manually by human resources.') % {'empl_name': self.name, })
            return attendance

    @api.model
    def register_attendance(self, card_code, action_date=None):
        """ ATTENTION!!! Overrides OCA/hr/hr_attendance_rfid/hr_employee.py/register_attendance original method in order tho add
                the action_date parameter. By default (action date is now) the original bevavior is guaranteed

        Register the attendance of the employee.
        :returns: dictionary
            'rfid_card_code': char
            'employee_name': char
            'employee_id': int
            'error_message': char
            'logged': boolean
            'action': check_in/check_out
        """

        res = {
            'rfid_card_code': card_code,
            'employee_name': '',
            'employee_id': False,
            'error_message': '',
            'logged': False,
            'action': 'FALSE',
        }
        employee = self.search([('rfid_card_code', '=', card_code)], limit=1)
        if employee:
            res['employee_name'] = employee.name
            res['employee_id'] = employee.id
        else:
            msg = _("No employee found with card %s") % card_code
            _logger.warning(msg)
            res['error_message'] = msg
            return res
        try:
            # -----------------------------------------------------------------
            # Original code:
            #  attendance = employee.attendance_action_change()
            attendance = employee.attendance_action_change(action_date=action_date)
            # -----------------------------------------------------------------
            if attendance:
                msg = _('Attendance recorded for employee %s') % employee.name
                _logger.debug(msg)
                res['logged'] = True
                if attendance.check_out:
                    res['action'] = 'check_out'
                else:
                    res['action'] = 'check_in'
                return res
            else:
                msg = _('No attendance was recorded for '
                        'employee %s') % employee.name
                _logger.error(msg)
                res['error_message'] = msg
                return res
        except Exception as e:
            res['error_message'] = e
            _logger.error(e)
        return res

    @api.model
    def register_attendance_min_secs_checks(self, card_code, action_date=None, min_secs_checks=None):
        """
        Before registering the attendance checks closer check in/out values
        :param card_code:
        :param action_date:
        :param min_secs_checks:
        :return:
        """
        if min_secs_checks:
            last_attendance = self.env['hr.attendance'].search([('employee_id.rfid_card_code', '=', card_code)],
                                                               order='check_in desc', limit=1)
            if last_attendance:
                last_check_date = last_attendance.check_out if last_attendance.check_out else last_attendance.check_in
                if not action_date:
                    action_date = fields.Datetime.now()
                difference_secs = (fields.Datetime.from_string(action_date) -
                                   fields.Datetime.from_string(last_check_date)).total_seconds()
                if difference_secs < min_secs_checks:
                    res = {
                        'rfid_card_code': card_code,
                        'employee_name': '',
                        'employee_id': False,
                        'error_message': _('Cannot register attendance because the action date (%s) is too close '
                                           'to the last check in/out date (%s)') % (action_date, last_check_date),
                        'logged': False,
                        'action': 'FALSE',
                    }
                    return res

        return self.register_attendance(card_code, action_date=action_date)
