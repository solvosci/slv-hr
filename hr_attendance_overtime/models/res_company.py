# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    after_calendar_min_tolerance_minutes = fields.Integer(
        'HR attendance overtime minimum tolerance (minutes)',
        default=0)
