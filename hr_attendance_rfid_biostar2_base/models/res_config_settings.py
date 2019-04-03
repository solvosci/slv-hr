# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    active_biostar2_server_id = fields.Many2one(
        'base.external.dbsource',
        string='Active Biostar2 server',
        related='company_id.biostar2_server_id')
    module_hr_attendance_rfid_biostar2_checks = fields.Boolean(
        'Enable BioStar2 check in/check out')
