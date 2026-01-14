# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    def write(self, vals):
        if 'supported_attachment_ids' in vals and \
                self.employee_id.user_id.id == self.env.user.id and \
                self.validation_type == 'no_validation' and \
                self.state == 'validate':
            res = super(HrLeave, self.sudo()).write(vals)
        else:
            res = super(HrLeave, self).write(vals)
        return res
