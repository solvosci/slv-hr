# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class Message(models.Model):
    _inherit = 'mail.message'

    def create(self, vals_list):
        res = super(Message, self).create(vals_list)
        leave_ids = res.filtered(lambda x: x.model == 'hr.leave' and x.attachment_ids).mapped("res_id")
        if leave_ids:
            leave_ids = self.env["hr.leave"].browse(leave_ids)
            leave_ids.filtered(lambda x: not x.has_attachment).sudo().write({"has_attachment": True})
        return res
