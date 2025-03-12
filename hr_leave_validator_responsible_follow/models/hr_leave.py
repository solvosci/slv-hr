# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from odoo import models, _
from pytz import timezone, UTC


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def activity_update(self):
        # Duplicated code from https://github.com/odoo/odoo/blob/4cc086d330b73514fbc64a7fcf22d8a7a9f1b691/addons/hr_holidays/models/hr_leave.py#L1112
        # to send a notification to the responsible person assigned to the hr.leave.type if the validation type is "Both" 
        for holiday in self.filtered(lambda x: x.holiday_status_id.validation_type == 'both'):
            start = UTC.localize(holiday.date_from).astimezone(timezone(holiday.employee_id.tz or 'UTC'))
            end = UTC.localize(holiday.date_to).astimezone(timezone(holiday.employee_id.tz or 'UTC'))
            note = _('New %s Request created by %s from %s to %s') % (holiday.holiday_status_id.name, holiday.create_uid.name, start, end)
            if holiday.state == 'confirm':
                holiday.activity_schedule(
                    'hr_holidays.mail_act_leave_approval',
                    note=note,
                    user_id=holiday.holiday_status_id.responsible_id.id or self.env.user.id)
            elif holiday.state == 'validate1':
                holiday.activity_feedback(['hr_holidays.mail_act_leave_approval'])
                holiday.activity_schedule(
                    'hr_holidays.mail_act_leave_second_approval',
                    note=note,
                    user_id=holiday.holiday_status_id.responsible_id.id or self.env.user.id)
        super(HrLeave, self).activity_update()

    def message_subscribe(self, partner_ids=None, channel_ids=None, subtype_ids=None):
        if self.holiday_status_id.validation_type == 'both':
            responsible_id = self.holiday_status_id.responsible_id.partner_id.id
            if responsible_id and responsible_id not in partner_ids:
                partner_ids.append(responsible_id)
        return super(HrLeave, self).message_subscribe(partner_ids=partner_ids, channel_ids=channel_ids, subtype_ids=subtype_ids)
