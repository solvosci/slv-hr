# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, api


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(IrAttachment, self).create(vals_list)
        leave_ids = res.filtered(lambda x: x.res_model == 'hr.leave').mapped("res_id")
        if leave_ids:
            leave_ids = self.env["hr.leave"].browse(leave_ids)
            leave_ids.filtered(lambda x: not x.has_attachment).sudo().write({"has_attachment": True})
        return res

    def unlink(self):
        hr_leave_ids = self.env['hr.leave']
        for record in self.filtered(lambda x: x.res_model == 'hr.leave'):
            hr_leave_ids |= self.env['hr.leave'].browse(record.res_id).exists()
        res = super(IrAttachment, self).unlink()
        for record in hr_leave_ids:
            record.sudo().has_attachment = bool(record.message_attachment_count)
        return res
