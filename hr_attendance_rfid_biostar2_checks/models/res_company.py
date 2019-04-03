# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    biostar2_server_min_secs_between_checks = fields.Integer(
        'Biostar2 server minimum seconds between checks',
        default=10)

    biostar2_server_last_checkinout_timestamp = fields.Integer(
        'Biostar2 server last check in/out timestamp',
        default=0)

