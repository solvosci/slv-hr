# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, api


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model_create_multi
    def create(self, vals_list):
        res = self.browse()
        for vals in vals_list:
            if vals.get('res_model') == 'hr.leave' and vals.get('res_id'):
                hr_leave_id = self.env['hr.leave'].browse(vals['res_id'])

                if(hr_leave_id.employee_id.user_id.id == self.env.user.id and
                    hr_leave_id.validation_type == 'no_validation' and
                    hr_leave_id.state == 'validate'
                ):
                    res |= super(IrAttachment, self.sudo()).create(vals)
                else:
                    res |= super(IrAttachment, self).create(vals)
            else:
                res |= super(IrAttachment, self).create(vals)
        return res

    def unlink(self):
        res = self.browse()
        for attach in self:
            if (attach.res_model == 'hr.leave' and attach.res_id):
                hr_leave_id = self.env['hr.leave'].browse(attach.res_id)
                if hr_leave_id.exists():
                    if (
                        hr_leave_id.employee_id.user_id.id == self.env.user.id and
                        hr_leave_id.validation_type == 'no_validation' and
                        hr_leave_id.state == 'validate'
                    ):
                        res = super(IrAttachment, attach.sudo()).unlink()
            else:
                res = super(IrAttachment, attach).unlink()
        return res
