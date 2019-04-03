# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    biostar2_server_min_secs_between_checks = fields.Integer(
        'Minimum seconds between checks',
        related='company_id.biostar2_server_min_secs_between_checks')

    biostar2_server_last_checkinout_timestamp = fields.Integer(
        'Last check in/out timestamp',
        related='company_id.biostar2_server_last_checkinout_timestamp')
