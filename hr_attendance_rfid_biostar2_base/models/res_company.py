# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    biostar2_server_id = fields.Many2one(
        'base.external.dbsource',
        string='Biostar2 server',
        domain=[('connector', '=', 'mysql')],
        ondelete='restrict')
