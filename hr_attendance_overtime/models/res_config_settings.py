# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    after_calendar_min_tolerance_minutes = fields.Integer(
        'Overtime minimum tolerance',
        related='company_id.after_calendar_min_tolerance_minutes')
    module_hr_attendance_overtime_report_xlsx = fields.Boolean(
        'Overtime report in XLSX format')
