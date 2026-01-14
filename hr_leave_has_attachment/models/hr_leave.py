# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    has_attachment = fields.Boolean(compute='_compute_has_attachment', store=True)

    @api.depends('supported_attachment_ids')
    def _compute_has_attachment(self):
        for leave in self:
            leave.has_attachment = bool(leave.supported_attachment_ids)
